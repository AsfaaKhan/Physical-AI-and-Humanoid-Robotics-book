import React from 'react';
import clsx from 'clsx';
import Layout from '@theme-original/Layout';

export default function LayoutWrapper(props) {
  return (
    <Layout {...props}>
      {props.children}
    </Layout>
  );
}