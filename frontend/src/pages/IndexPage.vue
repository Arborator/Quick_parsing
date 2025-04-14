<template>
  <q-page class="background">
    <div class="q-pa-md">
      <q-card flat>
        <q-card-section class="q-pa-none">
          <q-card flat class="col bg-primary" style="width: 100%;">
            <q-card-section>
              <div class="text-h4 text-center text-white text-bold">
                About ArboratorGrew parser
              </div>
            </q-card-section>
            <q-card-section class="bg-white q-pa-md">
              <div class="text-justify text-body1">
                <p>
                  Description of ArboratorGrew parser
                </p>
              </div>
            </q-card-section>
          </q-card>
        </q-card-section>
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
<style>
  .background {
    background: #f1f1f1;
  }
</style>