<template>
  <q-page>
    <ParsingComponent @get-parsing="handleParsing" />
  </q-page>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import ParsingComponent from "src/components/ParsingComponent.vue";

export default defineComponent({
  name: "ParsingPage",
  components: {
    ParsingComponent,
  },
  methods: {
    handleParsing(samples: any) {
      this.$router.push({
        name: "results",
        params: { results: JSON.stringify(samples) },
      });
    },
  },
});
</script>