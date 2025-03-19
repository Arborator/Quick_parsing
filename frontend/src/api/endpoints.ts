///// we have used the same types for the endpoints used in arboratorgrew 
///// https://github.com/Arborator/arborator-frontend/blob/master/src/api/endpoints.d.ts


import  {
  ModelInfo_t,
  ScoresBest_t,
  ScoresHistory_t
}
from './backend_types';



interface ParserStateFailure_t {
  status: 'failure';
  error: string;
}

interface ParserList_t {
  status: 'success';
  data: {
      model_info: ModelInfo_t;
      scores_best: ScoresBest_t;
      scores_history: ScoresHistory_t;
  }[];
}

export type ParserList_RV = ParserStateFailure_t | ParserList_t;

interface ParseStatus_t {
  status: 'success';
  data:
      {
        ready: false;  
      }
      |
      {
          ready: true;
          model_info: ModelInfo_t;
      }   
}

export type ParseStatus_RV = ParserStateFailure_t | ParseStatus_t;