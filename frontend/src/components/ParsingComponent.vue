<template>
  <div class="row justify-center">
    <div class="col-12 col-sm-10 col-md-8 col-lg-6">
      <q-card flat class="q-pa-md">
        <q-separator />

        <q-card-section class="q-pa-sm">
          <div class="text-h4 text-center text-primary text-bold">
            Parsing Settings
          </div>
        </q-card-section>

        <q-card-section class="row items-center q-gutter-sm q-pa-sm">
          <div class="col-auto">
            <div class="text-subtitle2">
              We have {{ availableModels.length }} parsers available:
            </div>
          </div>
          <div class="col-12">
            <q-select
              outlined
              use-input
              hide-dropdown-icon
              :placeholder="parser ? '' : 'Select your model to parse'"
              v-model="parser"
              option-label="label"
              option-value="value"
              :options="filteredModels"
              @filter="filterModels"
              dense
              clearable
            >
              <template v-slot:selected-item="scope">
                <div
                  :tabindex="scope.tabindex"
                  class="selected-model-label text-primary text-weight-bold"
                >
                  {{ scope.opt.label }}
                </div>
              </template>
              <template v-slot:option="scope">
                <q-item
                  v-close-popup
                  v-bind="scope.itemProps"
                  clickable
                  ripple
                  dense
                >
                  <q-item-section>
                    <q-item-label>{{ scope.opt.label }}</q-item-label>
                    <q-item-label caption>{{
                      scope.opt.value.model_info?.language || ""
                    }}</q-item-label>
                  </q-item-section>
                  <q-item-section side>
                    <q-chip dense outline color="primary">
                      {{
                        parseFloat(
                          scope.opt.value.scores_best?.LAS_epoch || 0,
                        ).toFixed(3)
                      }}
                    </q-chip>
                  </q-item-section>
                </q-item>
              </template>
            </q-select>
          </div>
        </q-card-section>

        <q-card-section class="q-pa-sm">
          <q-tabs v-model="parsingOption">
            <q-tab
              :class="parsingOption === 'file' ? 'text-primary' : 'text-grey-6'"
              name="file"
            >
              <div>
                <q-icon name="file_present" size="20px" class="q-mb-xs" />
                <div class="text-subtitle2">File input</div>
              </div>
            </q-tab>
            <q-tab
              :class="parsingOption === 'text' ? 'text-primary' : 'text-grey-6'"
              name="text"
            >
              <div>
                <q-icon name="title" size="20px" class="q-mb-xs" />
                <div class="text-subtitle2">Text input</div>
              </div>
            </q-tab>
          </q-tabs>
          <q-tab-panels v-model="parsingOption">
            <q-tab-panel name="file">
              <q-file
                ref="fileInput"
                :model-value="uploadedFiles"
                label="Attach one or multiple files (.conllu, .txt)"
                accept=".conllu,.txt"
                use-chips
                outlined
                multiple
                input-style="height:100px"
                @update:model-value="fileInputUpdate"
                @remove="fileRemoved"
              >
              </q-file>
            </q-tab-panel>
            <q-tab-panel name="text" class="q-gutter-md">
              <q-input
                outlined
                v-model="textToParse"
                type="textarea"
                label="Text to parse"
                class="q-mb-sm"
              />
              <div class="row items-center q-gutter-sm">
                <div class="col-12">
                  <div class="text-subtitle2">Select text format to parse</div>
                </div>
                <div class="col-12">
                  <q-option-group
                    v-model="textFormat"
                    :options="textFormatOptions"
                    type="radio"
                    inline
                  />
                </div>
              </div>
            </q-tab-panel>
          </q-tab-panels>
        </q-card-section>

        <q-card-section v-if="parsingOption !== 'text'" class="q-pa-sm">
          <q-btn
            flat
            dense
            :icon="showAdvanced ? 'expand_less' : 'expand_more'"
            :label="showAdvanced ? 'Hide Advanced Settings' : 'Show Advanced Settings'"
            @click="showAdvanced = !showAdvanced"
            class="text-primary text-bold"
          />
        </q-card-section>

        <q-card-section v-if="parsingOption !== 'text' && showAdvanced" class="q-pa-sm bg-grey-1">
          <div class="row items-center q-gutter-sm">
            <div class="col-12">
              <div class="text-subtitle2">
                Select CONLL columns to keep while parsing
              </div>
            </div>

            <div class="col-12">
              <q-option-group
                v-model="columnsToKeep"
                :options="conllColumns.map((c) => ({ label: c, value: c }))"
                type="checkbox"
                inline
              />
            </div>
          </div>
        </q-card-section>

        <q-card-section class="row justify-center">
          <div class="row items-center q-gutter-sm">
            <div class="col-auto text-subtitle2 q-mr-md" v-if="parsingSentencesEstimate > 0">
              Estimated parse time: <strong>{{ estimatedParsingTimeMinutes() }}</strong> mn
            </div>
            <q-btn
              class="bg-secondary text-white text-bold q-my-sm"
              no-caps
              :disable="disableParseBtn"
              label="PARSE THE INPUT"
              @click="startParsing"
            />
          </div>
        </q-card-section>
        <q-separator />
      </q-card>
    </div>
  </div>
</template>
<script lang="ts">
import api from "src/api/backend-api";
import { notifyMessage } from "src/utils/notify";
import { ParsingSettings_t } from "src/api/backend_types";
import { defineComponent } from "vue";

const TIMEOUT_TASK_STATUS_CHECKER = 1000 * 60 * 60 * 3; // 3 hours
const REFRESH_RATE_TASK_STATUS_CHECKER = 1000 * 10; // 10 seconds
const KIR_PARSER_SENT_PER_SEC_SPEED = 140; 

export default defineComponent({
  name: "ParsingComponent",
  data() {
    const uploadedFiles: File[] = [];
    const textToParse: string = "";
    const parser: any = null;
    const taskTimeStarted: number = 0;
    const availableModels: any[] = [];
    const filteredModels: any[] = [];
    const columnsToKeep: string[] = [];
    const conllColumns: string[] = [
      "LEMMA",
      "UPOS",
      "XPOS",
      "FEATS",
      "HEAD",
      "DEPREL",
    ];
    const parsedSamples: { [key: string]: string } = {};
    return {
      uploadedFiles,
      parsingSentencesEstimate: 0,
      textToParse,
      parser,
      parsingOption: "file",
      resultViewOption: "conll",
      textFormatOptions: [
        { label: "Plain text", value: "plainText" },
        { label: "Vertical", value: "vertical" },
        { label: "Horizontal", value: "horizontal" },
      ],
      textFormat: "plainText",
      availableModels,
      filteredModels,
      columnsToKeep,
      conllColumns,
      taskTimeStarted,
      parsedSamples,
      disableUpload: false,
      showAdvanced: false,
      taskIntervalChecker: null as
        | null
        | ReturnType<typeof setTimeout>
        | ReturnType<typeof setInterval>,
      inProgressNotify: null as null | (() => void),
    };
  },
  computed: {
    disableParseBtn() {
      if (this.parser === null || this.disableUpload) return true;
      if (this.parsingOption === "file") return this.uploadedFiles.length === 0;
      if (this.parsingOption === "text") return this.textToParse.trim() === "";
      return true;
    },
  },
  mounted() {
    this.getModels();
    this.EstimatedSentences();
  },
  watch: {
    uploadedFiles() {
      this.EstimatedSentences();
    },
    textToParse() {
      this.EstimatedSentences();
    },
    parsingOption() {
      this.EstimatedSentences();
    },
  },
  methods: {
    async checkExtension() {
      const extension = /^.*\.(conllu|txt)$/i;
      this.disableUpload = false;
      for (const file of this.uploadedFiles) {
        if (!extension.test(file.name)) {
          notifyMessage(
            `You have to upload .conllu or .txt file`,
            5000,
            "warning",
          );
          this.disableUpload = true;
          return;
        }
      }
    },
    async getModels() {
      try {
        const response = await api.getParsers();
        if (
          response?.data?.status === "success" &&
          Array.isArray(response.data.data) &&
          response.data.data.length > 0
        ) {
          this.availableModels = response.data.data.map((model) => {
            return { label: model.model_info.project_name, value: model };
          });
        } else {
          const mock1 = {
            model_info: { project_name: "Mock Parser A", language: "en" },
            scores_best: { LAS_epoch: 0.912 },
          };
          const mock2 = {
            model_info: { project_name: "Mock Parser B", language: "fr" },
            scores_best: { LAS_epoch: 0.845 },
          };
          this.availableModels = [
            { label: mock1.model_info.project_name, value: mock1 },
            { label: mock2.model_info.project_name, value: mock2 },
          ];
          notifyMessage("No parsers", 7000, "info");
        }
      } catch (error: any) {
        const mock1 = {
          model_info: { project_name: "Mock Parser A", language: "en" },
          scores_best: { LAS_epoch: 0.912 },
        };
        const mock2 = {
          model_info: { project_name: "Mock Parser B", language: "fr" },
          scores_best: { LAS_epoch: 0.845 },
        };
        this.availableModels = [
          { label: mock1.model_info.project_name, value: mock1 },
          { label: mock2.model_info.project_name, value: mock2 },
        ];
        const msg =
          error?.response?.data?.message || error?.message || String(error);
        notifyMessage(
          `Failed to load parsers, using mocks — ${msg}`,
          8000,
          "warning",
        );
      } finally {
        this.filteredModels = this.availableModels;
        try {
          this.saveParsingInputs();
        } catch (e) {
          notifyMessage('Failed to save previous parsing inputs', 5000, 'warning');
        }
      }
    },
    filterModels(val: string, update: (callback: () => void) => void) {
      if (val === "") {
        update(() => {
          this.filteredModels = this.availableModels;
        });
        return;
      }
      update(() => {
        const needle = val.toLowerCase();
        this.filteredModels = this.availableModels.filter(
          (v) => v.label.toLowerCase().indexOf(needle) > -1,
        );
      });
    },
    safeNormalize(text: string | null | undefined) {
      if (!text) return "";
      if (typeof (String.prototype as any).normalize === "function") {
        try {
          return (text as any).normalize("NFC");
        } catch (e) {
          return text;
        }
      }
      return text;
    },
    async startParsing() {
      try {
        const payload = {
          parsingOption: this.parsingOption,
          textToParse: this.textToParse,
          textFormat: this.textFormat,
          columnsToKeep: this.columnsToKeep,
          parserValue: this.parser?.value || null,
          uploadedFiles: (this.uploadedFiles || []).map((f: File) => f.name),
        };
        sessionStorage.setItem("parsingInputs", JSON.stringify(payload));
      } catch (e) {
        notifyMessage("Failed to store parsing inputs locally; continuing parsing",5000,"warning");
      }
      const parsingSettings: ParsingSettings_t = {
        keep_heads: this.columnsToKeep.includes("HEAD") ? "EXISTING" : "NONE",
        keep_upos: this.columnsToKeep.includes("UPOS") ? "EXISTING" : "NONE",
        keep_feats: this.columnsToKeep.includes("FEATS") ? "EXISTING" : "NONE",
        keep_xpos: this.columnsToKeep.includes("XPOS") ? "EXISTING" : "NONE",
        keep_deprels: this.columnsToKeep.includes("DEPREL")
          ? "EXISTING"
          : "NONE",
        keep_lemmas: this.columnsToKeep.includes("LEMMA") ? "EXISTING" : "NONE",
      };
      if (this.parsingOption === "text") {
        let payloadText = this.safeNormalize(this.textToParse);
        payloadText = payloadText.replace(/\r/g, "");
        if (this.textFormat === "vertical") {
          payloadText = payloadText.replace(/\n{3,}/g, "\n\n");
          if (!payloadText.endsWith("\n\n")) payloadText = payloadText + "\n\n";
        }

        const payload = {
          text: payloadText,
          option: this.textFormat,
          model: this.parser?.value || this.parser,
          parsingSettings,
        };

        this.taskTimeStarted = Date.now();
        api
          .parserParseStart(payload)
          .then((response) => {
            if (response.data.status === "failure") {
              notifyMessage(
                "Parsing could not start : " + response.data.error,
                10000,
                "negative",
              );
            } else {
              try {
                this.inProgressNotify = notifyMessage("Parsing in progress... Don't reload the page", 0, "info");
              } catch (e) {
                this.inProgressNotify = null;
              }
              const parseTaskId = response.data.data.parse_task_id;
              this.taskIntervalChecker = setInterval(() => {
                setTimeout(this.checkParserStatus(parseTaskId) as any, 10);
              }, REFRESH_RATE_TASK_STATUS_CHECKER);
            }
          })
          .catch((error) => {
            notifyMessage(error, 10000, "negative");
          });
        return;
      }

      const form = new FormData();
      for (const file of this.uploadedFiles) {
        form.append("files", file);
      }
      form.append("text_to_parse", this.textToParse);
      form.append("text_format", this.textFormat);
      form.append("model", JSON.stringify(this.parser.value));
      form.append("parsingSettings", JSON.stringify(parsingSettings));

      this.taskTimeStarted = Date.now();

      api
        .parserParseStart(form)
        .then((response) => {
          if (response.data.status === "failure") {
            notifyMessage(
              "Parsing could not start : " + response.data.error,
              10000,
              "negative",
            );
          } else {
            try {
              this.inProgressNotify = notifyMessage("Parsing in progress... Don't reload the page", 0, "info");
            } catch (e) {
              this.inProgressNotify = null;
            }
            const parseTaskId = response.data.data.parse_task_id;
            this.taskIntervalChecker = setInterval(() => {
              setTimeout(this.checkParserStatus(parseTaskId) as any, 10);
            }, REFRESH_RATE_TASK_STATUS_CHECKER);
          }
        })
        .catch((error) => {
          notifyMessage(error, 10000, "negative");
        });
    },
    checkParserStatus(taskId: string) {
      const data = { task_id: taskId };
      api
        .parserParseStatus(data)
        .then((response) => {
          if (response.data.status === "failure") {
            if (this.inProgressNotify) {
              try { this.inProgressNotify(); } catch (e) {}
              this.inProgressNotify = null;
            }
            notifyMessage(response.data.error, 10000, "negative");
            this.clearCurrentTask();
          } else if (response.data.data.ready) {
            this.clearCurrentTask();
            if (this.inProgressNotify) {
              try { this.inProgressNotify(); } catch (e) {}
              this.inProgressNotify = null;
            }
            this.parsedSamples = response.data.data.parsed_samples;
            this.$emit("get-parsing", this.parsedSamples);
            notifyMessage("Sentences parsing ended!", 3000, "positive");
          } else if (
            Date.now() - this.taskTimeStarted >
            TIMEOUT_TASK_STATUS_CHECKER
          ) {
            this.clearCurrentTask();
            if (this.inProgressNotify) {
              try { this.inProgressNotify(); } catch (e) {}
              this.inProgressNotify = null;
            }
          } else if (taskId === "PARSING") {
            window.onbeforeunload = function () {
              return "You have already started parsing, if you leave the page the changes will not be saved";
            };
          }
        })
        .catch((error) => {
          if (this.inProgressNotify) {
            try { this.inProgressNotify(); } catch (e) {}
            this.inProgressNotify = null;
          }
          notifyMessage(error, 10000, "negative");
          this.clearCurrentTask();
        });
    },
    clearCurrentTask() {
      if (this.taskIntervalChecker !== null) {
        clearInterval(this.taskIntervalChecker);
      }
    },

    fileInputUpdate(newFile: FileList | File[] | File | null) {
      const toArray = (f: any): File[] =>
        !f
          ? []
          : typeof FileList !== "undefined" && f instanceof FileList
            ? Array.from(f)
            : Array.isArray(f)
              ? f
              : [f];

      const income = toArray(newFile);
      const exist: File[] = this.uploadedFiles || [];

      if (income.length < exist.length) {
        this.uploadedFiles = income;
      } else {
        const present = exist.slice();
        for (const f of income) {
          if (!present.some((e) => e.name === f.name)) {
            present.push(f);
          }
        }
        this.uploadedFiles = present;
      }

      this.checkExtension();

      const refComp: any = this.$refs.fileInput;
      if (refComp && typeof refComp.reset === "function") refComp.reset();
      else if (refComp && refComp.$el) {
        const input = refComp.$el.querySelector("input[type=file]");
        if (input) input.value = "";
      }
    },

    fileRemoved(file: File) {
      this.uploadedFiles = (this.uploadedFiles || []).filter(
        (f) => !(f.name === file.name),
      );
      this.checkExtension();
    },

    async EstimatedSentences() {
      try {
        let total = 0;
        if (this.parsingOption === 'file' && this.uploadedFiles && this.uploadedFiles.length > 0) {
          const readFile = (this.uploadedFiles || []).map((f: File) => {
            return new Promise<string>((resolve) => {
              const read = new FileReader();
              read.onload = () => resolve(String(read.result || ''));
              read.onerror = () => resolve('');
              read.readAsText(f);
            });
          });
          const contents = await Promise.all(readFile);
          for (const [i, content] of contents.entries()) {
            const file = this.uploadedFiles[i];
            const name = file?.name || '';
            if (/\.conllu$/i.test(name)) {
              const blocks = content.split(/\n\s*\n+/).filter((b) => b.trim().length > 0);
              total += blocks.length;
            } else {
              const sent = content.split(/[\.\!\?]+\s+/).filter((s) => s.trim().length > 0);
              total += sent.length;
            }
          }
        } else if (this.parsingOption === 'text' && (this.textToParse || '').trim().length > 0) {
          const text = this.textToParse;
          const sent = text.split(/[\.\!\?]+\s+/).filter((s) => s.trim().length > 0);
          total = sent.length || 1;
        }
        this.parsingSentencesEstimate = total;
      } catch (e) {
        this.parsingSentencesEstimate = 0;
      }
    },

    estimatedParsingTimeMinutes() {
      const init_s = 60;
      const parsingEstimatedTime_s = this.parsingSentencesEstimate / KIR_PARSER_SENT_PER_SEC_SPEED;
      const total_s = init_s + parsingEstimatedTime_s;
      return Math.max(0, Math.ceil(total_s / 60));
    },

    saveParsingInputs() {
      try {
        const raw = sessionStorage.getItem("parsingInputs");
        if (!raw) return;
        const state = JSON.parse(raw);
        if (!state) return;
        if (state.parsingOption) this.parsingOption = state.parsingOption;
        if (state.textToParse) this.textToParse = state.textToParse;
        if (state.textFormat) this.textFormat = state.textFormat;
        if (state.columnsToKeep) this.columnsToKeep = state.columnsToKeep;
        if (state.parserValue) {
          const found = (this.availableModels || []).find((m: any) => {
            try {
              return JSON.stringify(m.value) === JSON.stringify(state.parserValue);
            } catch (e) {
              return m.label === state.parserValue?.model_info?.project_name;
            }
          });
          if (found) this.parser = found;
        }
        if (Array.isArray(state.uploadedFiles) && state.uploadedFiles.length > 0) {
          const first = state.uploadedFiles[0];
          if (typeof first === "string") {
            try {
              const filename: File[] = state.uploadedFiles.map((name: string) => new File([""], name, { type: "text/plain" }));
              this.uploadedFiles = filename;
            } catch (e) {
              this.uploadedFiles = [];
            }
          } else {
            const recreated: File[] = [];
            for (const sf of state.uploadedFiles) {
              try {
                const blob = new Blob([sf.content], { type: sf.type || "text/plain" });
                const f = new File([blob], sf.name, { type: sf.type || "text/plain" });
                recreated.push(f);
              } catch (e) {
                notifyMessage('Failed to restore one of the uploaded files', 5000, 'warning');
              }
            }
            this.uploadedFiles = recreated;
          }
        }
      } catch (e) {
        notifyMessage('Failed to restore previous parsing inputs', 5000, 'warning');
      }
    },
  },
});
</script>