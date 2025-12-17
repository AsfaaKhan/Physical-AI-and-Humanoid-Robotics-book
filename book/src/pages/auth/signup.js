import React from 'react';
import Layout from '@theme/Layout';
import Signup from '../../components/Auth/Signup';

function SignupPage() {
  const handleSignupSuccess = () => {
    // Redirect to home or profile page after successful signup
    window.location.href = '/';
  };

  return (
    <Layout title="Sign Up" description="Create an account to get personalized content">
      <div className="container margin-vert--lg">
        <div className="row">
          <div className="col col--6 col--offset-3">
            <Signup onSignupSuccess={handleSignupSuccess} />
          </div>
        </div>
      </div>
    </Layout>
  );
}

export default SignupPage;