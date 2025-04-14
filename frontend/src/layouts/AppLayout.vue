<template>
  <q-layout view="hHh Lpr fFf">
    <q-header class="q-pa-md">
      <q-bar class="row q-gutter-md justify-evenly bg-primary" style="height: 7.5vh;">
        <q-btn flat href="https://arborator.grew.fr/" :ripple="false" type="a">
          <div class="q-btn__content text-center col items-center q-anchor--skip row">
            <img alt="Arborator" src="/svg/arborator.grew.white.svg" style="height: 4vh" />
          </div>
        </q-btn>
        <q-space />
        <q-btn flat href="https://www.unicaen.fr/projet_de_recherche/automated/" :ripple="false" type="a">
          <div class="q-btn__content text-center col items-center q-anchor--skip row">
            <img alt="Arborator" src="/images/logo_automated.png" style="height: 6vh;" />
          </div>
        </q-btn>
      </q-bar>
    </q-header>
    <q-page-container> <router-view /> </q-page-container>
  </q-layout>

</template>
<script lang="ts">
import { defineComponent } from 'vue';

export default defineComponent({
  name: 'AppLayout',
});

</script>