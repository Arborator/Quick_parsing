import { Notify } from 'quasar';


export function notifyMessage(message: string, timeout: number, type: string) {
    Notify.create({
        message, 
        timeout, 
        position: 'top',
        type: type,
        closeBtn: 'X',
    })
}