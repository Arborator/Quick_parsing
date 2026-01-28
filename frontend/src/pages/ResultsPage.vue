<template>
  <div class="row justify-center">
    <div class="col-12 col-sm-10 col-md-8 col-lg-6">
      <q-card flat class="q-pa-md">
        <q-separator />

        <q-card-section class="q-pa-sm">
          <div class="text-h4 text-center text-primary text-bold">
            Parsing Results
          </div>
        </q-card-section>
        <q-card-section class="row justify-start">
          <q-btn
            flat
            icon="arrow_back"
            label="Back"
            @click="$router.back()"
            class="q-mb-md"
          />
        </q-card-section>
      </q-card>
    </div>
  </div>
  <div class="justify-center">
    <q-card-section class="q-pa-sm">
          <ResultView
            v-if="parsedSamples && Object.keys(parsedSamples).length > 0"
            :parsedSamples="parsedSamples"
          />
          <div v-else class="row justify-center">
            <q-card flat bordered class="col-12">
              <q-card-section>
                <div class="text-h6 text-center text-grey">
                  No results available
                </div>
              </q-card-section>
            </q-card>
          </div>
    </q-card-section>
    <q-separator />
  </div>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import { notifyMessage } from 'src/utils/notify';
import ResultView from "src/components/ResultView.vue";

export default defineComponent({
  name: "ResultsPage",
  components: {
    ResultView,
  },
  data() {
    return {
      parsedSamples: {},
    };
  },
  mounted() {
    const routeParam = (this.$route.params && (this.$route.params as any).results) ||
      (this.$route.query && (this.$route.query as any).results);

    if (routeParam) {
      try {
        this.parsedSamples = JSON.parse(routeParam as string);
        return;
      } catch (e) {
          console.warn('Failed to parse results from route param/query', e);
          notifyMessage('Could not parse results from route — falling back to stored results', 5000, 'warning');
      }
    }

    try {
      const stored = localStorage.getItem('parsedSamples');
      if (stored) {
        this.parsedSamples = JSON.parse(stored);
      }
    } catch (e) {
        console.warn('Failed to access localStorage for parsedSamples', e);
        notifyMessage('Could not retrieve stored parsing results', 5000, 'warning');
    }
  },
});
</script>