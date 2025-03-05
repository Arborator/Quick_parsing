import axios from 'axios';
import { boot } from 'quasar/wrappers';

import api from '../api/backend-api';


export default boot(({ app }) => {
 
  app.config.globalProperties.$axios = axios;
  app.config.globalProperties.$api = api;
  
});

export { api };
