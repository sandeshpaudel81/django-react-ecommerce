import React, { useState, useEffect } from 'react'
import { Row, Col } from 'react-bootstrap'
import { useDispatch, useSelector } from 'react-redux'

import { listProducts } from '../actions/productActions'
import Product from '../components/Product'
import Loader from '../components/Loader'
import Message from '../components/Message'

function HomeScreen() {
    const dispatch = useDispatch()
    // get list of products from state
    const productList = useSelector(state => state.productList)
    // destructuring productList state component into error message, loading status and actual data (products)
    const { error, loading, products} = productList

    useEffect(() => {
        // dispatch action to call api for fetching all products and save in the state   
        dispatch(listProducts())
    }, [dispatch])

    return (
        <div>
            <h1>Latest Products</h1>
            {loading ? <Loader />               /* if product is loading, show loader */
                : error ? <Message variant='danger'>{error}</Message>               /* if error is found, show error message */
                    :
                    <Row>                                        
                        {products.map(product => (                      /* if products are available, show products */
                            <Col key={product._id} sm={12} md={6} lg={4} xl={3}>
                                <Product product={product}/>
                            </Col>
                        ))}
                    </Row>
            }
        </div>
    )
}

export default HomeScreen
