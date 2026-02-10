<template>
  <q-page>
    <div class="q-pa-xs">
      <MapComponent class="q-mb-xs" />
      <div class="q-pa-xs">
        <ParsingComponent @get-parsing="handleParsing" />
      </div>
    </div>
  </q-page>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import { notifyMessage } from 'src/utils/notify';
import ParsingComponent from "src/components/ParsingComponent.vue";
import MapComponent from "src/components/MapComponent.vue";

export default defineComponent({
  name: "ParsingPage",
  components: {
    ParsingComponent,
    MapComponent,
  },
  methods: {
    handleParsing(samples: any) {
      try {
        sessionStorage.setItem('parsedSamples', JSON.stringify(samples));
      } catch (e: any) {
        console.warn('Failed to save parsedSamples to sessionStorage', e);
        notifyMessage('Failed to store results locally; continuing navigation', 5000, 'warning');
      }
      this.$router.push({ name: 'results' });
    },
  },
});
</script>