import React from 'react';
import Layout from '@theme/Layout';
import Signin from '../../components/Auth/Signin';

function SigninPage() {
  const handleSigninSuccess = () => {
    // Redirect to home or profile page after successful signin
    window.location.href = '/';
  };

  return (
    <Layout title="Sign In" description="Sign in to access your personalized content">
      <div className="container margin-vert--lg">
        <div className="row">
          <div className="col col--6 col--offset-3">
            <Signin onSigninSuccess={handleSigninSuccess} />
          </div>
        </div>
      </div>
    </Layout>
  );
}

export default SigninPage;