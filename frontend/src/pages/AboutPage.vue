<template>
  <div class="row justify-center q-mt-lg">
    <div class="col-12 col-sm-10 col-md-8 col-lg-6">
      <q-card flat class="q-pa-md">
        <q-separator />

        <q-card-section class="q-pa-sm">
          <div class="text-h4 text-center text-primary text-bold">
            About Parser
          </div>
        </q-card-section>

        <q-card-section class="q-pa-sm">
          <p class="text-body1">parser description goes here</p>
        </q-card-section>

        <q-separator />
      </q-card>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from "vue";

export default defineComponent({
  name: "AboutPage",
});
</script>