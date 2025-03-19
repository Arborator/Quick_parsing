import axios from 'axios';
import { ParserList_RV, ParseStatus_RV } from './endpoints';


export const API = axios.create({
    baseURL: process.env.DEV ? '/api' : `${process.env.API}/api`,
    timeout: 50000,
    withCredentials: false,
});

export default {
    getParsers() {
        return API.get<ParserList_RV>("parser/list");
    }, 
    parserParseStart(data: any) {
        return API.post("parser/start", data);
    }, 
    parserParseStatus(data: any) {
        return API.post<ParseStatus_RV>("parser/status", data);
    }

}