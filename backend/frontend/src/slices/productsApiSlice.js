import { PRODUCTS_URL } from '../constants';
import { apiSlice } from './apiSlice';

export const productSlice = apiSlice.injectEndpoints({
  endpoints: (builder) => ({
    // useGetAllProductsQuery func get all products pagination
    getAllProducts: builder.query({
      query: ({ keyword, pageNumber }) => ({
        url: `${PRODUCTS_URL}`,
        method: 'GET',
        params: { keyword, pageNumber },
      }),keepUnusedDataFor: 5,
      providesTags: ['Product'],
    }),
    // useGetProductsQuery func no pagination
    getProducts: builder.query({
      query: ({ keyword }) => ({
        url: PRODUCTS_URL,
        params: { keyword },
      }),
      keepUnusedDataFor: 5,
      //providesTags: ['Product'], // for cache invalidation, removed in pagination
    }),
    // useGetProductDetailsQuery func
    getProductDetails: builder.query({
      query: (productId) => ({
        url: `${PRODUCTS_URL}/${productId}/`,
      }),
      keepUnusedDataFor: 5,
    }),
    // admin useCreateProductMutation func (create product)
    createProduct: builder.mutation({
      query: () => ({
        url: `${PRODUCTS_URL}/create/`,
        method: 'POST',
      }),
      invalidatesTags: ['Product'],
    }),
    updateProduct: builder.mutation({
      query: (data) => ({
        url: `${PRODUCTS_URL}/update/${data.productId}/`,
        method: 'PUT',
        body: data,
      }),
      invalidatesTags: ['Product'],
    }),
    // admin upload pic builder
    uploadProductImage: builder.mutation({
      query: (data) => ({
        url: `${PRODUCTS_URL}/upload/`,
        method: 'POST',
        body: data,
      }),
    }),
    // admin useDeleteProductMutation func (delete product)
    deleteProduct: builder.mutation({
      query: (productId) => ({
        url: `${PRODUCTS_URL}/delete/${productId}/`,
        method: 'DELETE',
      }),
      invalidatesTags: ['Product'], // for cache invalidation
    }),
    createReview: builder.mutation({
      query: (data) => ({
        url: `${PRODUCTS_URL}/review/${data.productId}/`,
        method: 'POST',
        body: data,
      }),
      invalidatesTags: ['Product'],
    }),
    getTopProducts: builder.query({
      query: () => `${PRODUCTS_URL}/top/`,
      keepUnusedDataFor: 5,
    }),
    // update product countInStock
    updateProductCountInStock: builder.mutation({
      query: ({data, userInfo}) => ({
        url: `${PRODUCTS_URL}/${data.productId}/updateinstock`,
        //url: `http://localhost:3001/api/products/${data.productId}/updateinstock`,
        method: 'PUT',
        body: {data, userInfo},
      }),
      invalidatesTags: ['Product'], // for cache invalidation
    }),
  }),
});

export const { useGetProductsQuery, useGetProductDetailsQuery, useCreateProductMutation, 
  useUpdateProductMutation, useUploadProductImageMutation, useDeleteProductMutation,
  useCreateReviewMutation, useGetTopProductsQuery, useUpdateProductCountInStockMutation, useGetAllProductsQuery, } = productSlice;