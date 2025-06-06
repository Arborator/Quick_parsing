<template>
  <q-card flat bordered>

    <q-card-section>
      <div class="text-h4 text-center text-primary text-bold">
        Parsing Results
      </div>
    </q-card-section>

    <q-card-section class="row q-gutter-md">
      <q-btn outline class="col" color="primary" label="Download output" @click="downloadZip()" />
      <q-select class="col" v-model="parsedSample" outlined label="Select a sample" :options="Object.keys(parsedSamples)" @update:model-value="getTrees" />
    </q-card-section>

    <q-card-section>
      <q-tabs v-model="resultViewOption" class="bg-primary text-white">
        <q-tab name="conll" label="Conll view"></q-tab>
        <q-tab name="tree" label="Tree view"></q-tab>
      </q-tabs>
      <q-tab-panels v-model="resultViewOption" class="background">
        <q-tab-panel name="conll">
          <pre>{{ parsedSamples[parsedSample] }}</pre>
        </q-tab-panel>
        <q-tab-panel name="tree">
          <q-virtual-scroll
            :items="conlls"
            :style="{ height: '100vh' }"
            :key="conlls.length"
            :virtual-scroll-item-size="100"
            :virtual-scroll-slice-size="10"
          >
            <template #default="{ item }">
              <TreeComponent :sentenceConll="item" />
            </template>
          </q-virtual-scroll>
        </q-tab-panel>
      </q-tab-panels>
    </q-card-section>

  </q-card>

</template>
<script lang="ts">
import JSZip from 'jszip';
import { saveAs } from 'file-saver';

import TreeComponent from './TreeComponent.vue';

import { defineComponent, PropType } from 'vue';

export default defineComponent({
  name: 'ResultView',
  components: {
    TreeComponent,
  },
  props: {
    parsedSamples: {
      type: Object as PropType<{ [key: string]: string }>,
      required: true,
    },
  },
  data() {
    const parsedSample: string = '';
    const resultViewOption: string = 'conll';
    const conlls: string[] = [];
    return {
      parsedSample,
      resultViewOption,
      conlls,
    };
  },
  mounted() {
    this.parsedSample = Object.keys(this.parsedSamples)[0] as string;
    this.getTrees();
  },
  methods: {
    getTrees() {
      const allTrees = this.parsedSamples[this.parsedSample]?.split('\n\n') as string[];
      this.conlls = allTrees.length > 50 ? allTrees.slice(0, 50) : allTrees;
    },
    async downloadZip() {
      const zip = new JSZip();

      for (const [fileName, content] of Object.entries(this.parsedSamples)) {
        zip.file(`${fileName}.conllu`, content as string);
      }

      const zipBlob = await zip.generateAsync({ type: "blob" });
      saveAs(zipBlob, "parsed_files.zip");
    }
  }
});


</script>