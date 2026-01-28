<template>
  <div class="row justify-center q-mt-lg">
    <div class="col-12 col-sm-10 col-md-8 col-lg-6">
      <q-card flat class="q-pa-md">
        <q-separator />

        <q-card-section class="q-pa-sm">
          <div class="text-h4 text-center text-primary text-bold">
            Parsing Results
          </div>
        </q-card-section>
                <q-card-section class="row justify-start">
          <q-btn flat icon="arrow_back" label="Back" @click="$router.back()" class="q-mb-md" />
        </q-card-section>

        <q-card-section class="q-pa-sm">
          <ResultView v-if="parsedSamples && Object.keys(parsedSamples).length > 0" :parsedSamples="parsedSamples" />
          <div v-else class="row justify-center">
            <q-card flat bordered class="col-12">
              <q-card-section>
                <div class="text-h6 text-center text-grey">No results available</div>
              </q-card-section>
            </q-card>
          </div>
        </q-card-section>

        <q-separator />
      </q-card>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import ResultView from 'src/components/ResultView.vue';

export default defineComponent({
  name: 'ResultsPage',
  components: {
    ResultView,
  },
  data() {
    return {
      parsedSamples: {},
    };
  },
  mounted() {
    const params = this.$route.params.results;
    if (params) {
      this.parsedSamples = JSON.parse(params as string);
    }
  },
});
</script>