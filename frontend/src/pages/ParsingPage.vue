<template>
  <q-page>
    <div class="q-pa-xs">
      <MapComponent ref="mapComponent" @language-selected="selectLanguageFromMap" />
      <div class="q-pa-xs">
        <ParsingComponent ref="parsingComponent" @get-parsing="handleParsing" @language-changed="selectLanguageOnParsingComponent" />
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
  data() {
    return {
      parsingComponentRef: null as any,
    };
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
    selectLanguageFromMap(languageData: any) {
      const languageName = languageData.name;
      const parsingComp = this.$refs.parsingComponent as any;
      const mapComp = this.$refs.mapComponent as any;
      
      if (mapComp) {
        mapComp.selectLanguageOnMap(languageName, parsingComp.availableLanguages);
      }
      
      const matchingParser = parsingComp.allParsers.find((parser: string) =>
        parser.toLowerCase().includes(languageName.toLowerCase())
      );
      
      if (matchingParser) {
        const match = matchingParser.match(/^[A-Z]+_(.+)-([^-]+)$/);
        const language = match ? match[1] : undefined;
        if (language) {
          parsingComp.selectedLanguage = language;
          parsingComp.selectedTreebank = '';
        }
      } else {
        console.warn(`Aucun parser trouvé pour: ${languageName}`);
      }
    },
    selectLanguageOnParsingComponent(eventData: any) {
      const selectedLanguage = eventData.language;
      const parsingComp = this.$refs.parsingComponent as any;
      const mapComp = this.$refs.mapComponent as any;
      
      if (mapComp) {
        mapComp.selectLanguageOnMap(selectedLanguage, parsingComp.availableLanguages);
      }
      
      const languageExists = parsingComp.availableLanguages.includes(selectedLanguage);
      if (!languageExists) {
        parsingComp.selectedLanguage = '';
        parsingComp.selectedTreebank = '';
      }
    },
  },
});
</script>
