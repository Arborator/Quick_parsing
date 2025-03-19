///// We are using the same types that are used in arboratorgrew to handle the data communicated between the frontend and the backend
///// https://github.com/Arborator/arborator-frontend/blob/master/src/api/backend-types.ts

export interface ModelInfo_t {
    project_name: string;
    model_id: string;
}
  
interface DataDescription_T {
    n_train_sents: number;
    n_test_sents: number;
    n_train_batches: number;
    n_test_batches: number;
}
interface TrainingDiagnostics_t {
    data_description: DataDescription_T;
    epoch: number;
    saved: boolean;
    is_best_loss: boolean;
    is_best_LAS: boolean;
    epochs_without_improvement: number;
    stopping_early: boolean;
}
interface ScoresOneEpoch_t {
    LAS_epoch: number;
    LAS_chuliu_epoch: number;
    acc_head_epoch: number;
    acc_deprel_epoch: number;
    acc_uposs_epoch: number;
    acc_xposs_epoch: number;
    acc_feats_epoch: number;
    acc_lemma_scripts_epoch: number;
    loss_head_epoch: number;
    loss_deprel_epoch: number;
    loss_xposs_epoch: number;
    loss_feats_epoch: number;
    loss_lemma_scripts_epoch: number;
    loss_epoch: number;
    data_description: TrainingDiagnostics_t | null;
    training_diagnostics: TrainingDiagnostics_t;
}

export type ScoresBest_t = ScoresOneEpoch_t;

export type ScoresHistory_t = ScoresOneEpoch_t[];
