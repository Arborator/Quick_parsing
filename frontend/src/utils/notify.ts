import { Notify } from 'quasar';


export function notifyMessage(message: string, timeout: number) {
    Notify.create({
        message, 
        timeout, 
        position: 'top',
        type: 'positive',
        closeBtn: 'X',
    })
}

export function notifyError(message: string, timeout: number) {
    Notify.create({
        message, 
        timeout,
        position: 'top',
        type: 'negative',
        closeBtn: 'X',
    })
}