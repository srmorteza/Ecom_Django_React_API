import React, { useState, useEffect } from 'react';
import { getProducts } from './helper/coreapicalls';

function Home() {
    const [product, getProducts] = useState([]);
    const [error, setError] = useState(false);

    return (
        <div>
            <h1>
                Home component

            </h1>
        </div>
    );
}

export default Home;