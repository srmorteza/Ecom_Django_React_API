import { API } from '../../Backend'


export const getProducts = () => {
    return fetch(`${API}product`, { method: 'get' })
        .then(response => {
            return response.json
        })
        .catch(err => {
            console.log(err)
        })

}