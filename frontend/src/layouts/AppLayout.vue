<template>
    <q-layout view="hHh Lpr fFf">
        <q-header style="height: 5vh;">
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