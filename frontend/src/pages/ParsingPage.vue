<template>
  <q-page>
    <ParsingComponent @get-parsing="handleParsing" />
  </q-page>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import { notifyMessage } from 'src/utils/notify';
import ParsingComponent from "src/components/ParsingComponent.vue";

export default defineComponent({
  name: "ParsingPage",
  components: {
    ParsingComponent,
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