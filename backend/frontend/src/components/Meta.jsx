import { Helmet } from 'react-helmet-async';

const Meta = ({ title, description, keywords }) => {
  return (
    <Helmet>
      <title>{title}</title>
      <meta name='description' content={description} />
      <meta name='keyword' content={keywords} />
    </Helmet>
  );
};

Meta.defaultProps = {
  title: 'abylch',
  description: 'Customized eCommerce / Shopping Cart Application made with reactjs, django, postgres, redux-toolkit',
  keywords: 'eCommerce, reactjs, django, postgres, redux, abylch',
};

export default Meta;
