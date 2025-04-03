<template>
  <q-card flat>
    <q-card-section class="row q-gutter-md">
      <div class="col">
        <q-select
          class="col"
          outlined
          use-input
          label="Available models"
          v-model="parser"
          option-label="label"
          option-value="value"
          emit-label
          :options="filteredModels"
          @filter="filterModels"
        >
        </q-select>
      </div>
      <div class="col">
        <q-select
          v-if="parsingOption !== 'text'"
          class="col"
          label="Select columns to keep"
          v-model="columnsToKeep"
          outlined
          use-chips
          multiple
          :options="conllColumns"
        >
        </q-select>
      </div>
    </q-card-section>
    <q-card-section>
      <q-tabs v-model="parsingOption" dense active-color="primary">
        <q-tab name="file" label="File input"></q-tab>
        <q-tab name="text" label="Text input"></q-tab>
      </q-tabs>
      <q-separator />
      <q-tab-panels v-model="parsingOption">
        <q-tab-panel name="file">
          <q-file
            v-model="uploadedFiles"
            label="Attach one or multiple files"
            use-chips
            outlined
            multiple
            input-style="height:100px"
            @update:model-value="checkExtension"
          >
          </q-file>
        </q-tab-panel>
        <q-tab-panel name="text">
          <q-input
            v-model="textToParse"
            outlined
            type="textarea"
            label="Text to parse"
          >
          </q-input>
        </q-tab-panel>
      </q-tab-panels>
    </q-card-section>
    <q-card-section>
      <q-btn no-caps :disable="disableParseBtn" color="primary" label="Parse" @click="startParsing" />
    </q-card-section>
  </q-card>
</template>
<script lang="ts">
import api from 'src/api/backend-api';
import { notifyMessage } from 'src/utils/notify';
import { ParsingSettings_t } from 'src/api/backend_types';
import { defineComponent } from 'vue';

const TIMEOUT_TASK_STATUS_CHECKER = 1000 * 60 * 60 * 3; // 3 hours
const REFRESH_RATE_TASK_STATUS_CHECKER = 1000 * 10; // 10 seconds

export default defineComponent({
  name: 'ParsingComponent',
  data() {
    const uploadedFiles: File[] = [];
    const textToParse: string =  '';
    const parser: any = null;
    const taskTimeStarted: number = 0;
    const availableModels: any[] = [];
    const filteredModels: any[] = [];
    const columnsToKeep: string[] = [];
    const conllColumns: string[] = ['LEMMA', 'UPOS', 'XPOS', 'FEATS', 'HEAD', 'DEPREL'];
    const parsedSamples: { [key: string]: string } = {};
    return {
      uploadedFiles,
      textToParse,
      parser,
      parsingOption: 'file',
      resultViewOption: 'conll',
      availableModels,
      filteredModels,
      columnsToKeep,
      conllColumns,
      taskTimeStarted, 
      parsedSamples,
      disableUpload: false,
      taskIntervalChecker: null as null | ReturnType<typeof setTimeout> | ReturnType<typeof setInterval>,
    }
  },
  computed: {
    disableParseBtn() {
      return (this.parser === null || this.uploadedFiles.length === 0 || this.disableUpload) && (this.textToParse === "" || this.parser === null);
    }
  },
  mounted() {
    this.getModels();
  },
  methods: {
    async checkExtension() {
      const extension = /^.*\.(conllu)$/;
      this.disableUpload = false;
      for (const file of this.uploadedFiles) {
        if (!extension.test(file.name)) {
          notifyMessage(`You have to upload Conll file`, 5000, 'warning');
          this.disableUpload = true;
          return 
        }
      }
    },
    getModels() {
      api
        .getParsers()
        .then((response) => {
          if (response.data.status === 'success') {
            this.availableModels = response.data.data.map((model) => {
              return { label: model.model_info.project_name, value: model};
            });
          }
        })
        .catch((error) => {
          notifyMessage(error.response.data.message, 10000, 'negative');
        })
    }, 
    filterModels(val: string, update: (callback: () => void) => void) {
      if (val === '') {
        update(() => {
          this.filteredModels = this.availableModels;
        });
        return;
      }
      update(() => {
        const needle = val.toLowerCase();
        this.filteredModels = this.availableModels.filter((v) => v.label.toLowerCase().indexOf(needle) > -1);
      });
    },
    startParsing() {
      const parsingSettings: ParsingSettings_t = {
        keep_heads: this.columnsToKeep.includes('HEAD') ? 'EXISTING' : 'NONE',
        keep_upos: this.columnsToKeep.includes('UPOS') ? 'EXISTING' : 'NONE',
        keep_feats: this.columnsToKeep.includes('FEATS') ? 'EXISTING' : 'NONE',
        keep_xpos: this.columnsToKeep.includes('XPOS') ? 'EXISTING' : 'NONE',
        keep_deprels: this.columnsToKeep.includes('DEPREL') ? 'EXISTING' : 'NONE',
        keep_lemmas: this.columnsToKeep.includes('LEMMA') ? 'EXISTING' : 'NONE',

      }
      const form = new FormData();

      for (const file of this.uploadedFiles) {
        form.append('files', file);
      }

      form.append('text_to_parse', this.textToParse);
      form.append('model', JSON.stringify(this.parser.value));
      form.append('parsingSettings', JSON.stringify(parsingSettings));

      this.taskTimeStarted = Date.now();

      api
        .parserParseStart(form)
        .then((response) => {
          if (response.data.status === 'failure') {
            notifyMessage('Parsing could not start : ' + response.data.error , 10000, 'negative');
          } else {
            notifyMessage('Sentences parsing started', 10000, 'positive');
            const parseTaskId = response.data.data.parse_task_id;
            this.taskIntervalChecker = setInterval(() => {
              setTimeout(this.checkParserStatus(parseTaskId) as any, 10);
            }, REFRESH_RATE_TASK_STATUS_CHECKER);
          }
        })
        .catch((error) => {
          notifyMessage(error, 10000, 'negative');
        });
    },
    checkParserStatus(taskId: string) {
      const data = { task_id: taskId }
      api
        .parserParseStatus(data)
        .then((response) => {
          if (response.data.status === 'failure') {
            notifyMessage(response.data.error, 10000, 'negative');
          } else if (response.data.data.ready) {
            this.clearCurrentTask();
            this.parsedSamples = response.data.data.parsed_samples;
            this.$emit('get-parsing', this.parsedSamples);
            notifyMessage('Sentences parsing ended!', 0, 'positive');  
          }
          else if (Date.now() - this.taskTimeStarted > TIMEOUT_TASK_STATUS_CHECKER) {
            this.clearCurrentTask();
          }
          else if (taskId === 'PARSING') {
            window.onbeforeunload = function () {
              return 'You have already started parsing, if you leave the page the changes will not be saved';
            }
          }
        })
        .catch((error) => {
          notifyMessage(error, 10000, 'negative');
          this.clearCurrentTask();
        });
    },
    clearCurrentTask() {
      if (this.taskIntervalChecker !== null) {
        clearInterval(this.taskIntervalChecker);
      }
    }, 
    
  }

});
</script>