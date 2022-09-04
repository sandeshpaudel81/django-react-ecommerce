import React, {useState, useEffect} from 'react'
import { Link } from 'react-router-dom'
import { Form, Button } from 'react-bootstrap'
import { useDispatch, useSelector } from 'react-redux'
import Loader from '../components/Loader'
import Message from '../components/Message'
import FormContainer from '../components/FormContainer'
import { listProductDetails, updateProduct } from '../actions/productActions'
import { PRODUCT_UPDATE_RESET } from '../constants/productConstants'


function ProductEditScreen({match, history}) {

    const productId = match.params.id

    const [name, setName] = useState('')
    const [price, setPrice] = useState(0)
    const [image, setImage] = useState('')
    const [brand, setBrand] = useState('')
    const [category, setCategory] = useState('')
    const [countInStock, setCountInStock] = useState(0)
    const [description, setDescription] = useState('')

    const dispatch = useDispatch()

    const productDetails = useSelector(state => state.productDetails)
    const {error, loading, product} = productDetails

    const productUpdate = useSelector(state => state.productUpdate)
    const {error: errorUpdate, loading: loadingUpdate, success: successUpdate} = productUpdate

    useEffect(() => {
        if (successUpdate){
            dispatch({type: PRODUCT_UPDATE_RESET})
            history.push('/admin/productlist')
        } else {
            if (!product.name || product._id !== Number(productId)){
                dispatch(listProductDetails(productId))
            } else {
                setName(product.name)
                setPrice(product.price)
                setImage(product.image)
                setBrand(product.brand)
                setCategory(product.category)
                setCountInStock(product.countInStock)
                setDescription(product.description)
            }
        }
    }, [product, dispatch, productId, history, successUpdate])

    const submitHandler = (e) => {
        e.preventDefault()
        dispatch(updateProduct({
            _id:productId,
            name,
            price,
            image,
            brand,
            category,
            countInStock,
            description
        }))
    }

    return( 
        <div>
            <Link to='/admin/productlist'>
                Go Back
            </Link>
            <FormContainer>
                <h1>Edit Product</h1>
                {loadingUpdate && <Loader/>}
                {errorUpdate && <Message variant='danger'>{errorUpdate}</Message>}
                { loading ? <Loader /> : error ? (
                    <Message variant='danger'>{error}</Message>
                ): (
                    <Form onSubmit={submitHandler}>

                        <Form.Group className='mt-2' controlId='name'>
                            <Form.Label>Name</Form.Label>
                            <Form.Control
                                type='name' 
                                placeholder='Enter Name' 
                                value={name} 
                                onChange={(e) => setName(e.target.value)}
                            >
                            </Form.Control>
                        </Form.Group>

                        <Form.Group className='mt-2' controlId='price'>
                            <Form.Label>Price</Form.Label>
                            <Form.Control
                                type='number' 
                                placeholder='Enter Price' 
                                value={price} 
                                onChange={(e) => setPrice(e.target.value)}
                            >
                            </Form.Control>
                        </Form.Group>

                        <Form.Group className='mt-2' controlId='image'>
                            <Form.Label>Image</Form.Label>
                            <Form.Control
                                type='text' 
                                placeholder='Enter Image' 
                                value={image} 
                                onChange={(e) => setImage(e.target.value)}
                            >
                            </Form.Control>
                        </Form.Group>

                        <Form.Group className='mt-2' controlId='brand'>
                            <Form.Label>Name</Form.Label>
                            <Form.Control
                                type='text' 
                                placeholder='Enter brand' 
                                value={brand} 
                                onChange={(e) => setBrand(e.target.value)}
                            >
                            </Form.Control>
                        </Form.Group>

                        <Form.Group className='mt-2' controlId='countInStock'>
                            <Form.Label>Stock</Form.Label>
                            <Form.Control
                                type='number' 
                                placeholder='Enter stock' 
                                value={countInStock} 
                                onChange={(e) => setCountInStock(e.target.value)}
                            >
                            </Form.Control>
                        </Form.Group>

                        <Form.Group className='mt-2' controlId='category'>
                            <Form.Label>Category</Form.Label>
                            <Form.Control
                                type='text' 
                                placeholder='Enter category' 
                                value={category} 
                                onChange={(e) => setCategory(e.target.value)}
                            >
                            </Form.Control>
                        </Form.Group>

                        <Form.Group className='mt-2' controlId='description'>
                            <Form.Label>Description</Form.Label>
                            <Form.Control
                                type='text' 
                                placeholder='Enter description' 
                                value={description} 
                                onChange={(e) => setDescription(e.target.value)}
                            >
                            </Form.Control>
                        </Form.Group>

                        <Button className='mt-4' type='submit' variant='primary'>
                            Update
                        </Button>
                    </Form>
                )}

                
            </FormContainer>
        </div>
    )
}

export default ProductEditScreen
