<template>
  <div>
    <div class="sentencebox">
      <svg ref="svgWrapper"></svg>
    </div>
  </div>
</template>

<script lang="ts">

import { SentenceSVG, defaultSentenceSVGOptions } from 'dependencytreejs/src/SentenceSVG';
import { SentenceCaretaker, ReactiveSentence } from 'dependencytreejs/src/ReactiveSentence';
import { setThemeMode as setThemeModeForDepTrees } from 'dependencytreejs/src/StylesheetHandler';
import { PropType, defineComponent } from 'vue';



export default defineComponent({
  props: {
    reactiveSentence: {
      type: Object as PropType<ReactiveSentence>,
      required: true,
    },
    conll: {
      type: String as PropType<string>,
      required: true,
    },
  },
  data() {
    const sentenceSVG: SentenceSVG = null as unknown as SentenceSVG;
    const sentenceCaretaker: SentenceCaretaker = null as unknown as SentenceCaretaker;
    return {
      sentenceSVG,
      sentenceCaretaker,
    };
  },
  mounted() {
    this.reactiveSentence.attach(this);
    this.reactiveSentence.fromSentenceConll(this.conll);
    
    const sentenceSVGOptions = defaultSentenceSVGOptions();
    sentenceSVGOptions.shownFeatures = ['FORM', 'UPOS']
    sentenceSVGOptions.drawEnhancedTokens = true;
    sentenceSVGOptions.interactive = false
    sentenceSVGOptions.arcHeight = 40;
    sentenceSVGOptions.tokenSpacing = 25;

    const svgWrapper = this.$refs.svgWrapper as SVGElement;
    this.sentenceSVG = new SentenceSVG(svgWrapper, this.reactiveSentence, sentenceSVGOptions);

    this.sentenceCaretaker = new SentenceCaretaker(this.reactiveSentence);
    this.sentenceCaretaker.backup();
    setThemeModeForDepTrees('LIGHT', true);
  },
  methods: {
    update() {
      const newMetaText = this.reactiveSentence.getSentenceText();
      console.log('update', newMetaText);
    },

  },
});
</script>

<style>
* {
  --depLevelHeight: 30;
}
</style>