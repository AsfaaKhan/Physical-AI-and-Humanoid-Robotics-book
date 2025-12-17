import React, { useState, useEffect } from 'react';
import { useAuth } from '../../contexts/AuthContext';

const Profile = () => {
  const { user, background, updateProfile, getProfile, isLoading } = useAuth();
  const [formData, setFormData] = useState({
    softwareExperience: 'beginner',
    programmingBackground: 'none',
    hardwareKnowledge: 'none'
  });
  const [isEditing, setIsEditing] = useState(false);
  const [isSaving, setIsSaving] = useState(false);
  const [message, setMessage] = useState('');
  const [error, setError] = useState('');

  useEffect(() => {
    if (background) {
      setFormData({
        softwareExperience: background.software_experience || 'beginner',
        programmingBackground: background.programming_background || 'none',
        hardwareKnowledge: background.hardware_knowledge || 'none'
      });
    }
  }, [background]);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsSaving(true);
    setMessage('');
    setError('');

    try {
      const profileData = {
        background: {
          software_experience: formData.softwareExperience,
          programming_background: formData.programmingBackground,
          hardware_knowledge: formData.hardwareKnowledge
        }
      };

      const result = await updateProfile(profileData.background);

      if (result.success) {
        setMessage('Profile updated successfully!');
        setIsEditing(false);
        // Refresh profile data
        await getProfile();
      } else {
        setError(result.error || 'Failed to update profile');
      }
    } catch (err) {
      setError(err.message || 'An error occurred while updating profile');
    } finally {
      setIsSaving(false);
    }
  };

  const handleEditToggle = () => {
    if (isEditing) {
      // Cancel edit and revert to saved values
      if (background) {
        setFormData({
          softwareExperience: background.software_experience || 'beginner',
          programmingBackground: background.programming_background || 'none',
          hardwareKnowledge: background.hardware_knowledge || 'none'
        });
      }
    }
    setIsEditing(!isEditing);
  };

  if (isLoading && !user) {
    return <div>Loading...</div>;
  }

  if (!user) {
    return <div>Please sign in to view your profile.</div>;
  }

  return (
    <div className="profile-container">
      <h2>User Profile</h2>

      <div className="profile-info">
        <h3>Account Information</h3>
        <p><strong>Email:</strong> {user.email}</p>
        <p><strong>Member Since:</strong> {user.created_at ? new Date(user.created_at).toLocaleDateString() : 'N/A'}</p>
      </div>

      <div className="profile-background">
        <h3>Background Information</h3>

        {isEditing ? (
          <form onSubmit={handleSubmit} className="profile-form">
            <div className="form-group">
              <label htmlFor="softwareExperience">Software Experience:</label>
              <select
                id="softwareExperience"
                name="softwareExperience"
                value={formData.softwareExperience}
                onChange={handleInputChange}
              >
                <option value="beginner">Beginner</option>
                <option value="intermediate">Intermediate</option>
                <option value="expert">Expert</option>
              </select>
            </div>

            <div className="form-group">
              <label htmlFor="programmingBackground">Programming Background:</label>
              <select
                id="programmingBackground"
                name="programmingBackground"
                value={formData.programmingBackground}
                onChange={handleInputChange}
              >
                <option value="none">None</option>
                <option value="basic">Basic</option>
                <option value="intermediate">Intermediate</option>
                <option value="advanced">Advanced</option>
              </select>
            </div>

            <div className="form-group">
              <label htmlFor="hardwareKnowledge">Hardware Knowledge:</label>
              <select
                id="hardwareKnowledge"
                name="hardwareKnowledge"
                value={formData.hardwareKnowledge}
                onChange={handleInputChange}
              >
                <option value="none">None</option>
                <option value="basic">Basic</option>
                <option value="intermediate">Intermediate</option>
                <option value="advanced">Advanced</option>
              </select>
            </div>

            <div className="form-actions">
              <button type="submit" disabled={isSaving}>
                {isSaving ? 'Saving...' : 'Save Changes'}
              </button>
              <button type="button" onClick={handleEditToggle}>
                Cancel
              </button>
            </div>
          </form>
        ) : (
          <div className="background-display">
            <p><strong>Software Experience:</strong> {formData.softwareExperience}</p>
            <p><strong>Programming Background:</strong> {formData.programmingBackground}</p>
            <p><strong>Hardware Knowledge:</strong> {formData.hardwareKnowledge}</p>
            <button onClick={handleEditToggle} className="edit-button">
              Edit Profile
            </button>
          </div>
        )}

        {message && <div className="success-message">{message}</div>}
        {error && <div className="error-message">{error}</div>}
      </div>
    </div>
  );
};

export default Profile;