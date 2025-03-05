<template>
  <q-page>
    <div class="q-pa-md">
      <q-card flat>
        <ParsingComponent></ParsingComponent>
      </q-card>
    </div>
    <q-footer>
      <q-item-label caption class="text-center text-grey-3">
        v1.0 (2024)
      </q-item-label>
    </q-footer>
  </q-page>
</template>
<script>
import ParsingComponent from 'src/components/ParsingComponent.vue';
import { defineComponent } from 'vue';

export default defineComponent({
  name: 'IndexPage',
  components: {
    ParsingComponent
  },

})


</script>