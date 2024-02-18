import { Row, Col } from 'react-bootstrap';
import { useParams } from 'react-router-dom';
import { useGetAllProductsQuery } from '../slices/productsApiSlice';
import { Link } from 'react-router-dom';
import Product from '../components/Product';
import Loader from '../components/Loader';
import Message from '../components/Message';
//import Paginate from '../components/Paginate';
//import ProductCarousel from '../components/ProductCarousel';
import Meta from '../components/Meta';

const HomeScreen = () => {
  // const { pageNumber, keyword } = useParams();
  const { keyword } = useParams();

  const { data: products, isLoading, error } = useGetAllProductsQuery({
    keyword,
    // pageNumber,
  });

  return (
    <>
      {/* {!keyword ? (
        <ProductCarousel />
      ) : (
        <Link to='/' className='btn btn-light mb-4'>
          Go Back
        </Link>
      )} */}
      {isLoading ? (
        <Loader />
      ) : error ? (
        <Message variant='danger'>
          {error?.data?.detail || error.error || error?.data?.message}
        </Message>
      ) : (
        <>
          <Meta />
          <h1>Latest Products</h1>
          <Row>
            {products.map((product) => (
              <Col key={product._id} sm={12} md={6} lg={4} xl={3}>
                <Product product={product} />
              </Col>
            ))}
          </Row>
          {/* <Paginate
            pages={data.pages}
            page={data.page}
            keyword={keyword ? keyword : ''}
          /> */}
        </>
      )}
    </>
  );
};

export default HomeScreen;
