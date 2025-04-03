<template>
  <q-page>
    <div class="q-pa-md">
      <q-card flat>
        <q-card-section>
          <ParsingComponent @get-parsing="getParsedSamples"></ParsingComponent>
        </q-card-section>
        <q-card-section v-if="Object.keys(parsedSamples).length > 0">
          <ResultView :parsedSamples="parsedSamples"></ResultView>
        </q-card-section>
      </q-card>
    </div>
    <q-footer>
      <q-item-label caption class="text-center text-grey-3">
        v1.0 (2024)
      </q-item-label>
    </q-footer>
  </q-page>
</template>
<script lang="ts">
import ParsingComponent from 'src/components/ParsingComponent.vue';
import ResultView from 'src/components/ResultView.vue';
import { defineComponent } from 'vue';

export default defineComponent({
  name: 'IndexPage',
  components: {
    ParsingComponent, 
    ResultView
  },
  data() {
    const parsedSamples: { [key: string]: string } = {};
    return {
      parsedSamples,
    };  
  },
  methods: {
    getParsedSamples(value: any) {
      this.parsedSamples = value;
    }
  }
});
</script>