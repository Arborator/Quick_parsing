<template>
  <q-card v-if="sentenceConll !==  ''" flat bordered class="scrollable q-pa-md">
    <q-card-section>
      <q-chip class="text-center" color="grey" dense>{{ sentId }}</q-chip>
      {{ sentenceText }}
    </q-card-section>
    <q-card-section>
      <TreeViewWrapper
        :conll="sentenceConll"
        :reactiveSentence="(reactiveSentence as ReactiveSentence)"
      />
    </q-card-section>
  </q-card>
</template>

<script lang="ts">
import TreeViewWrapper from './TreeViewWrapper.vue';
import { ReactiveSentence } from 'dependencytreejs/src/ReactiveSentence';
import { defineComponent, PropType } from 'vue';

export default defineComponent({
  name: 'TreeComponent',
  components: {
    TreeViewWrapper,
  },
  props: {
    sentenceConll: {
      type: String as PropType<string>,
      required: true,
    }
  }, 
  data() {
    const reactiveSentence: ReactiveSentence = null as unknown as ReactiveSentence;
    const sentenceText: string = '';
    const sentId: string | number = '';
    return {
      reactiveSentence,
      sentenceText,
      sentId,
    };
  }, 
  created() {
    this.reactiveSentence = new ReactiveSentence();
  },
  mounted() {
    this.sentenceText = this.reactiveSentence.getSentenceText();
    this.sentId = this.reactiveSentence.state.metaJson['sent_id'] as string;
  },
});
</script>
<style scoped>
  .scrollable {
    overflow-x: auto;
  }
</style>
