import React from 'react';
import Layout from '@theme/Layout';
import ChatbotWidget from '../ChatbotWidget';

export default function LayoutWrapper(props) {
  return (
    <>
      <Layout {...props}>
        {props.children}
      </Layout>
      <ChatbotWidget />
    </>
  );
}