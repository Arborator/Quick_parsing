import axios from 'axios';


export const API = axios.create({
    baseURL: process.env.DEV ? '/api' : `${process.env.API}/api`,
    timeout: 50000,
    withCredentials: false,
});

export default {
    getParsers() {
        return API.get("parser/list")
    }, 
    parserParseStart(data: any) {
        return API.post("parser/start", data)
    }, 
    parserParseStatus(data: any) {
        return API.post("parser/status", data)
    }

}