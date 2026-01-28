<template>
  <q-layout view="hHh Lpr fFf">
    <q-header class="q-pa-md">
      <q-bar
        class="row q-gutter-md justify-evenly bg-primary"
        style="height: 7.5vh"
      >
        <q-btn flat href="https://arborator.grew.fr/" :ripple="false" type="a">
          <div
            class="q-btn__content text-center col items-center q-anchor--skip row"
          >
            <img
              alt="Arborator"
              src="/svg/arborator.grew.white.svg"
              style="height: 4vh"
            />
          </div>
        </q-btn>
        <q-space />
        <q-btn
          flat
          href="https://autogramm.github.io/"
          :ripple="false"
          type="a"
        >
          <div
            class="q-btn__content text-center col items-center q-anchor--skip row"
          >
            <img
              alt="autogramm"
              src="/images/logo_autogramm.svg"
              style="height: 6vh"
            />
          </div>
        </q-btn>
        <q-btn
          flat
          href="https://www.unicaen.fr/projet_de_recherche/automated/"
          :ripple="false"
          type="a"
        >
          <div
            class="q-btn__content text-center col items-center q-anchor--skip row"
          >
            <img
              alt="Arborator"
              src="/images/logo_automated.png"
              style="height: 6vh"
            />
          </div>
        </q-btn>
      </q-bar>
    </q-header>

    <q-breadcrumbs class="q-pa-md bg-grey-2">
      <q-breadcrumbs-el v-for="t in tabs" :key="t.name" :label="t.label" />
    </q-breadcrumbs>

    <div class="row justify-center q-pa-lg">
      <q-tabs
        v-model="currentTab"
        dense
        class="text-primary"
        active-color="primary"
        indicator-color="primary"
        @update:model-value="navigateTo"
      >
        <q-tab
          v-for="t in tabs"
          :key="t.name"
          :name="t.name"
        >
          <div class="text-subtitle2 text-bold">{{ t.label }}</div>
        </q-tab>
      </q-tabs>
    </div>

    <q-separator />

    <q-page-container>
      <router-view />
    </q-page-container>
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
      routesMap: appTabs.reduce(
        (acc, t) => {
          (acc as any)[t.name] = t.path;
          return acc;
        },
        {} as { [key: string]: string },
      ),
    };
  },
  watch: {
    $route(to) {
      this.currentTab = this.getTabFromPath(to.path);
    },
  },
  mounted() {
    this.currentTab = this.getTabFromPath(this.$route.path);
  },
  methods: {
    navigateTo(tab: string) {
      const route = this.routesMap[tab];
      if (route) this.$router.push(route);
    },
    getTabFromPath(path: string) {
      for (const key in this.routesMap) {
        if (this.routesMap[key] === path) return key;
      }
      return "parsing";
    },
  },
});
</script>