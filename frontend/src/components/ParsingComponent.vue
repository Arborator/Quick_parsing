<template>
  <q-card flat>
    <q-card-section>
      <q-select
        outlined
        label="Available models"
        v-model="parser"
        :options="availableModels"
      >
      </q-select>
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
      <q-btn @click="startParsing">Parse</q-btn>

    </q-card-section>
  </q-card>
</template>
<script lang="ts">
import api from 'src/api/backend-api';
import { notifyError, notifyMessage } from 'src/utils/notify';
import { defineComponent } from 'vue';

const TIMEOUT_TASK_STATUS_CHECKER = 1000 * 60 * 60 * 3; // 3 hours
const REFRESH_RATE_TASK_STATUS_CHECKER = 1000 * 10; // 10 seconds

export default defineComponent({
  name: 'ParsingComponent',
  data() {
    const uploadedFiles: File[] = [];
    const textToParse: string =  '';
    const parser: string = '';
    const taskTimeStarted: number = 0;
    return {
      uploadedFiles,
      textToParse,
      parser,
      parsingOption: 'file',
      availableModels: [],
      taskTimeStarted, 
      taskIntervalChecker: null as null | ReturnType<typeof setTimeout> | ReturnType<typeof setInterval>,
    }
  },
  methods: {
    getModels() {
      api
        .getParsers()
        .then((response) => {
          if (response.data.status === 'success'){
            this.availableModels = response.data.models;
          }
        })
        .catch((error) => {
          notifyError(error.response.data.message, 10000);
        })
    }, 
    startParsing() {
      const form = new FormData()
      for (const file in this.uploadedFiles) {
        form.append('files', file)
      }
      form.append('text_to_parse', this.textToParse)
      form.append('model', this.parser)

      this.taskTimeStarted = Date.now();

      api
        .parserParseStart(form)
        .then((response) => {
          if (response.data.status === 'failure') {
            notifyError('Parsing could not start : ' + response.data.error , 10000);
          } else {
            notifyMessage('Sentences parsing started', 10000);
            const parseTaskId = response.data.data.parse_task_id;
            this.taskIntervalChecker = setInterval(() => {
              setTimeout(this.checkParserStatus(parseTaskId) as any, 10);
            }, REFRESH_RATE_TASK_STATUS_CHECKER);
          }
        })
        .catch((error) => {
          notifyError(error, 10000);
        });
    },
    checkParserStatus(taskId: string) {
      const data = { task_id: taskId }
      api
        .parserParseStatus(data)
        .then((response) => {
          if (response.data.status === 'failure') {
            notifyError(response.data.error, 10000);
          } else if (response.data.data.ready) {
            notifyMessage('Sentences parsing ended!', 0);
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
          console.log(error);
          this.clearCurrentTask();
        });
    },
    clearCurrentTask() {
      if (this.taskIntervalChecker !== null) {
        clearInterval(this.taskIntervalChecker);
      }
    }
  }

});
</script>