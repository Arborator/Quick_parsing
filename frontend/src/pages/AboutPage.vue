<template>
  <div class="row justify-center">
    <div class="col-12 col-sm-10 col-md-8 col-lg-6">
      <q-card flat class="q-pa-md">
        <q-separator />

        <q-card-section class="q-pa-sm">
          <div class="text-h4 text-center text-primary text-bold">
            About Parser
          </div>
        </q-card-section>
      </q-card>
    </div>
  </div>
  <q-page>
    <div class="q-pa-md">
      <div class="row justify-center">
        <div class="col-12 col-sm-11 col-md-9 col-lg-8">
          <q-card flat bordered class="q-mb-md">
            <q-card-section>
              <h2 class="text-h6 text-primary q-mt-none q-mb-md">Introduction</h2>
              <p class="text-body1 q-my-sm">
                <strong>SUD Parse</strong> is a service for syntactic analysis that uses models pretrained on 
                <a href="https://universaldependencies.org/" target="_blank">Universal Dependencies (UD)</a> and 
                <a href="https://surfacesyntacticud.org/" target="_blank">Surface Universal Dependencies (SUD)</a> corpora.
              </p>
              <p class="text-body1 q-my-sm">
                It can be used for parsing of sample sentences or small corpora (<router-link to="/parsing">Parsing</router-link> tab).
              </p>
              <p class="text-body1 q-my-sm">
                The results can be visualised as trees or as CONLLU files, which can be downloaded (<router-link to="/results">Results</router-link> tab).
              </p>
            </q-card-section>
          </q-card>

          <q-card flat bordered class="q-mb-md">
            <q-card-section>
              <h2 class="text-h6 text-primary q-mt-none q-mb-md">Description of the service</h2>
              <ul class="q-pl-md q-my-none">
                <li class="q-mb-sm text-body1">Parsing can be performed in the UD or SUD framework</li>
                <li class="q-mb-sm text-body1">Token limit for plain text input is 50,000 tokens (provided the anticipated number of sentences does not exceed 5,000). For  CONLLU or text file input the parser can process up to 100,000 tokens (if the number of sentences is not greater than 5,000).</li>
                <li class="q-mb-sm text-body1">
                  SUD Parse service uses 
                  <a href="https://github.com/kirianguiller/BertForDeprel" target="_blank">BertForDeprel</a> parser with 
                  <a href="https://huggingface.co/docs/transformers/model_doc/xlm-roberta" target="_blank">XLMRoBERTa</a> embeddings
                </li>
                <li class="q-mb-sm text-body1">
                  The model is selected first by language and then by training corpus. Models were trained on existing treebanks that contain 
                  more than 20,000 tokens only
                </li>
                <li class="q-mb-sm text-body1">
                  The performance of the model printed in brackets next to the name of the corpus can be used as an indication of the performance. 
                  It relates to the performance of the model trained on the dev part tested on the test part of the corpus. 
                  The performance is given using the standard measure of 
                  <a href="https://universaldependencies.org/conll18/evaluation.html" target="_blank">Labelled Attachment Score</a>. 
                  The model used in the service, however, was trained on the whole corpus (dev, train and test combined). 
                  On the principles of data split in UD, see <a href="https://universaldependencies.org/contributing/repository_files.html#data-split" target="_blank">here</a>.
                </li>
                <li class="q-mb-sm text-body1">
                  Information about the corpus on which the model was trained can be accessed by clicking on the Github link which appears 
                  next to the name of the selected model. The nature of the training corpus (genre, modality etc) can also be used as a criterion 
                  for the selection of the model.
                </li>
              </ul>
            </q-card-section>
          </q-card>

          <q-card flat bordered class="q-mb-md">
            <q-card-section>
              <h2 class="text-h6 text-primary q-mt-none q-mb-md">Sentence segmentation and tokenisation (plain text or text file upload)</h2>
              <p class="text-body1 q-my-sm">
                <p>Please note that automatic sentence segmentation (using strong punctuation) is performed automatically only for French language 
                models when "plain text" format is selected.</p>
              </p>
              <p class="text-body1 q-my-sm">
                <p>For other languages, "horizontal" or "vertical" format have to be selected. Each sentence begins on a new line in the horizontal 
                format and tokens are separated by spaces. Each token begins on a new line and sentences are separated by blank lines in the vertical 
                format. It is up to the user to prepare the data for processing.</p>
              </p>
            </q-card-section>
          </q-card>

                    <q-card flat bordered class="q-mb-lg">
            <q-card-section>
              <h2 class="text-h6 text-primary q-mt-none q-mb-md">Code and issues</h2>
              <p class="text-body1 q-my-sm">
                The code of the web interface is available at
                <a href="https://github.com/Arborator/Quick_parsing" target="_blank">https://github.com/Arborator/Quick_parsing.</a> </p>
                <p class="text-body1 q-my-sm"> You can report issues, send feature requests or questions to (<a href="https://github.com/Arborator/Quick_parsing/issues" target="_blank">Discussions</a> tab).
              </p>
            </q-card-section>
          </q-card>

          <q-card flat bordered class="q-mb-lg">
            <q-card-section>
              <h2 class="text-h6 text-primary q-mt-none q-mb-md">Acknowledgements</h2>
              <p class="text-body1 q-my-sm">
                The project was jointly funded by the <a href="https://autogramm.github.io/" target="_blank">Autogram project</a> (Agence Nationale de Recherche, 2022-2026) and the 
                <a href="https://www.unicaen.fr/projet_de_recherche/automated/" target="_blank">AUTOMATED project</a> (Normandy Region, 2023-2025). 
                The service was developed by Ramy Amrani and Khensa Daoudi. 
                BertForDeprel parser was developed by Killian Guiller.
              </p>
            </q-card-section>
          </q-card>

          <div class="text-center q-mb-lg">
            <p class="text-body1 text-grey-7">
              Detailed Help Page can be found <a href="https://arborator.github.io/arborator-documentation/#/parserQuick">here</a>
            </p>
          </div>
        </div>
      </div>
    </div>
  </q-page>
</template>

<script lang="ts">
import { defineComponent } from "vue";

export default defineComponent({
  name: "AboutPage",
});
</script>

<style scoped lang="scss">
a {
  color: #1976d2;
  text-decoration: none;

  &:hover {
    text-decoration: underline;
  }
}
</style>