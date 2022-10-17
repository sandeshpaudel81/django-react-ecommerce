// axios - used to send asynchronous HTTP requests to REST endpoints
import axios from 'axios'
// importing constants
import {
    CART_ADD_ITEM,
    CART_REMOVE_ITEM,
    CART_SAVE_SHIPPING_ADDRESS,
    CART_SAVE_PAYMENT_METHOD,
} from '../constants/cartConstants'

// action that dispatches reducer to add items to the cart
export const addToCart = (id, qty) => async (dispatch, getState) => {
    // get product from backend by id
    const {data} = await axios.get(`/api/products/${id}`)

    // dispatch type and payload to the cart reducer
    dispatch({
        type: CART_ADD_ITEM,
        payload: {
            product: data._id,
            name: data.name,
            image: data.image,
            price: data.price,
            countInStock: data.countInStock,
            qty
        }
    })

    // save cart items in local storage (get items from state using getState)
    localStorage.setItem('cartItems', JSON.stringify(getState().cart.cartItems))
}

// action that dispatches id of the product to cart reducer to remove it from cart
export const removeFromCart = (id) => (dispatch, getState) => {
    dispatch({
        type: CART_REMOVE_ITEM,
        payload: id,
    })

    // save cart items in local storage after removing the desired product (get items from state using getState)
    localStorage.setItem('cartItems', JSON.stringify(getState().cart.cartItems))
}

// action that dispatches shipping address data to the cart reducer to save in the store
export const saveShippingAddress = (data) => (dispatch) => {
    dispatch({
        type: CART_SAVE_SHIPPING_ADDRESS,
        payload: data,
    })

    // save shipping address in local storage
    localStorage.setItem('shippingAddress', JSON.stringify(data))
}

// action that dispatches payment method to the cart reducer to save in the store
export const savePaymentMethod = (data) => (dispatch) => {
    dispatch({
        type: CART_SAVE_PAYMENT_METHOD,
        payload: data,
    })

    // save payment method in local storage
    localStorage.setItem('paymentMethod', JSON.stringify(data))
}