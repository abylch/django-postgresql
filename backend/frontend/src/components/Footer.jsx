import { Container, Row, Col } from 'react-bootstrap';

const Footer = () => {
  const currentYear = new Date().getFullYear();

  return (
    <footer>
      <Container>
        <Row>
          <Col className='text-center py-3'>
            <p>abylch &copy; {currentYear}</p>
            <p>@e-Shop-Shop; e-commerce website using Django, React JS, Redux toolkit and PostgreSQL, and S3 bucket, e-commerce plataform template a work in progress, always evolving.</p>
          </Col>
        </Row>
      </Container>
    </footer>
  );
};
export default Footer;
