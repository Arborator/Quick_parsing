<template>
  <q-layout view="hHh Lpr fFf">
    <q-header class="bg-primary q-px-lg q-py-sm">
      <div class="row items-center q-gutter-lg" style="height: 70px">
        <q-btn flat href="https://arborator.grew.fr/" :ripple="false" type="a">
          <img
            alt="Arborator"
            src="/svg/arborator.grew.white.svg"
            style="height: 50px; object-fit: contain"
          />
        </q-btn>
        <q-space />

        <q-btn flat href="https://autogramm.github.io/" :ripple="false" type="a">
          <img
            alt="autogramm"
            src="/images/logo_autogramm.svg"
            style="height: 45px; object-fit: contain"
          />
        </q-btn>
        <q-btn flat href="https://www.unicaen.fr/projet_de_recherche/automated/" :ripple="false" type="a">
          <img
            alt="Automated"
            src="/images/logo_automated.png"
            style="height: 45px; object-fit: contain"
          />
        </q-btn>
      </div>
    </q-header>

    <q-breadcrumbs class="q-px-lg q-py-lg">
      <q-breadcrumbs-el v-for="t in tabs" :key="t.name" :label="t.label" />
    </q-breadcrumbs>

    <q-bar class="bg-white">
      <div class="row justify-center full-width">
        <q-tabs
          v-model="currentTab"
          dense
          class="text-primary"
          active-color="primary"
          indicator-color="primary"
          @update:model-value="navigateTo"
        >
          <q-tab v-for="t in tabs" :key="t.name" :name="t.name">
            <div class="text-subtitle2 text-bold">{{ t.label }}</div>
          </q-tab>
        </q-tabs>
      </div>
    </q-bar>

    <q-separator />

    <q-page-container>
      <router-view />
    </q-page-container>
    <div
      v-if="isParsingLocked"
      class="parsing-overlay"
      style="position:fixed;inset:0;background:rgba(0,0,0,0.6);z-index:9999;display:flex;align-items:center;justify-content:center"
    >
      <div style="text-align:center;color:white">
        <q-spinner-dots color="white" size="56px" />
        <div class="text-h6 q-mt-md">Parsing en cours — veuillez patienter</div>
      </div>
    </div>
  </q-layout>
</template>
<script lang="ts">
import { defineComponent } from "vue";
import { appTabs } from "src/router/routes";

export default defineComponent({
  name: "AppLayout",
  data() {
    return {
      currentTab: "parsing",
      tabs: appTabs,
      isParsingLocked: false,
      routesMap: appTabs.reduce((acc, t) => {
        (acc as any)[t.name] = (t as any).path || (t as any).href;
        return acc;
      }, {} as { [key: string]: string }),
    };
  },
  watch: {
    $route(to) {
      this.currentTab = this.getTabFromPath(to.path);
    },
  },
  mounted() {
    this.currentTab = this.getTabFromPath(this.$route.path);
    window.addEventListener("parsing-lock", this.handleParsingLock);
  },
  beforeUnmount() {
    window.removeEventListener("parsing-lock", this.handleParsingLock);
  },
    methods: {
      handleParsingLock(event: Event) {
        const parsing = event as CustomEvent;
        (this as any).isParsingLocked = Boolean(parsing.detail?.locked);
      },
      navigateTo(tab: string) {
        const route = this.routesMap[tab];
        if (!route) return;
        if (route.startsWith("http")) {
          window.open(route, "_blank");
        } else {
          this.$router.push(route);
        }
      },
      getTabFromPath(path: string) {
        for (const key in this.routesMap) {
          const val = this.routesMap[key];
          if (val === path) return key;
        }
        return "parsing";
      },
    },
});
</script>