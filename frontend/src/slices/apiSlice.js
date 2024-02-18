// apiSlice.js
// import { fetchBaseQuery, createApi } from '@reduxjs/toolkit/query/react';
// import { BASE_URL } from '../constants';
// import { logout } from './authSlice';

// const baseQuery = fetchBaseQuery({
//   baseUrl: BASE_URL,
//   prepareHeaders: (headers, { getState }) => {
//     const { userInfo } = getState().auth; // Get the token from the auth state
//     const token = userInfo ? userInfo.token : null; // Check if the token exists
//     console.log('Token:', token); // Log the token for debugging

//     if (token) {
//       headers.set('Authorization', `Bearer ${token}`);
//       console.log('Headers:', headers); // Log the headers for debugging
//     }

//     return headers;
//   },
// });


// async function baseQueryWithAuth(args, api, extraOptions) {

//   const result = await baseQuery(args, api, ...extraOptions);

//   console.log("from apiSlice.js result", result)

//   if (result.error && result.error.status === 401) {
//     api.dispatch(logout());
//   }

//   return result;
// }

// export const apiSlice = createApi({
//   baseQuery: baseQueryWithAuth,
//   tagTypes: ['Product', 'Order', 'User'],
//   endpoints: (builder) => ({}),
// });


import { fetchBaseQuery, createApi } from '@reduxjs/toolkit/query/react';
import { BASE_URL } from '../constants';

import { logout } from './authSlice'; // Import the logout action

// NOTE: code here has changed to handle when our JWT and Cookie expire.
// We need to customize the baseQuery to be able to intercept any 401 responses
// and log the user out
// https://redux-toolkit.js.org/rtk-query/usage/customizing-queries#customizing-queries-with-basequery

// const baseQuery = fetchBaseQuery({
//   baseUrl: BASE_URL,
// });

const baseQuery = fetchBaseQuery({
  baseUrl: BASE_URL,
  prepareHeaders: (headers, { getState }) => {
    const { userInfo } = getState().auth; // Get the token from the auth state
    const token = userInfo ? userInfo.token : null; // Check if the token exists
    console.log('Token:', token); // Log the token for debugging

    if (token) {
      headers.set('Authorization', `Bearer ${token}`);
      console.log('Headers:', headers); // Log the headers for debugging
    }

    return headers;
  },
});

async function baseQueryWithAuth(args, api, extra) {
  const result = await baseQuery(args, api, extra);
  console.log("from apiSlice.js args", args)
  console.log("from apiSlice.js api", api)
  console.log("from apiSlice.js extra", extra)
  console.log("from apiSlice.js result", result)

  // Dispatch the logout action on 401.
  if (result.error && result.error.status === 401) {
    api.dispatch(logout());
  }
  else console.log("error from apiSlice.js", result.error);

  return result;
}

export const apiSlice = createApi({
  baseQuery: baseQueryWithAuth, // Use the customized baseQuery
  tagTypes: ['Product', 'Order', 'User'],
  endpoints: (builder) => ({}),
});
