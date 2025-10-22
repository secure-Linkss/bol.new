import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { Label } from './ui/label';
import { Avatar, AvatarFallback, AvatarImage } from './ui/avatar';
import { Badge } from './ui/badge';
import { 
  User, 
  Mail, 
  Shield, 
  Calendar, 
  Key, 
  Upload,
  Save,
  X
} from 'lucide-react';
import { toast } from 'sonner';

const UserProfile = ({ user, onClose, onUpdate }) => {
  const [profileData, setProfileData] = useState({
    username: user?.username || '',
    email: user?.email || '',
    avatar_url: user?.avatar_url || '',
    subscription_plan: user?.subscription_plan || 'free',
    subscription_expires: user?.subscription_expires || null
  });
  
  const [passwordData, setPasswordData] = useState({
    current_password: '',
    new_password: '',
    confirm_password: ''
  });
  
  const [isEditingPassword, setIsEditingPassword] = useState(false);
  const [loading, setLoading] = useState(false);
  const [avatarFile, setAvatarFile] = useState(null);
  const [avatarPreview, setAvatarPreview] = useState(profileData.avatar_url);

  useEffect(() => {
    fetchProfileData();
  }, []);

  const fetchProfileData = async () => {
    try {
      const response = await fetch('/api/user/profile', {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      });
      
      if (response.ok) {
        const data = await response.json();
        setProfileData(data);
        setAvatarPreview(data.avatar_url);
      }
    } catch (error) {
      console.error('Error fetching profile:', error);
    }
  };

  const handleAvatarChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      if (file.size > 5 * 1024 * 1024) { // 5MB limit
        toast.error('File size must be less than 5MB');
        return;
      }
      
      setAvatarFile(file);
      const reader = new FileReader();
      reader.onloadend = () => {
        setAvatarPreview(reader.result);
      };
      reader.readAsDataURL(file);
    }
  };

  const handleProfileUpdate = async () => {
    setLoading(true);
    try {
      const formData = new FormData();
      formData.append('username', profileData.username);
      formData.append('email', profileData.email);
      
      if (avatarFile) {
        formData.append('avatar', avatarFile);
      }

      const response = await fetch('/api/user/profile', {
        method: 'PUT',
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        },
        body: formData
      });

      if (response.ok) {
        const data = await response.json();
        setProfileData(data);
        toast.success('Profile updated successfully!');
        if (onUpdate) onUpdate(data);
      } else {
        const errorData = await response.json();
        toast.error(errorData.error || 'Failed to update profile');
      }
    } catch (error) {
      console.error('Error updating profile:', error);
      toast.error('Failed to update profile');
    } finally {
      setLoading(false);
    }
  };

  const handlePasswordChange = async () => {
    if (passwordData.new_password !== passwordData.confirm_password) {
      toast.error('New passwords do not match');
      return;
    }

    if (passwordData.new_password.length < 8) {
      toast.error('Password must be at least 8 characters long');
      return;
    }

    setLoading(true);
    try {
      const response = await fetch('/api/user/change-password', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        },
        body: JSON.stringify({
          current_password: passwordData.current_password,
          new_password: passwordData.new_password
        })
      });

      if (response.ok) {
        toast.success('Password changed successfully!');
        setPasswordData({
          current_password: '',
          new_password: '',
          confirm_password: ''
        });
        setIsEditingPassword(false);
      } else {
        const errorData = await response.json();
        toast.error(errorData.error || 'Failed to change password');
      }
    } catch (error) {
      console.error('Error changing password:', error);
      toast.error('Failed to change password');
    } finally {
      setLoading(false);
    }
  };

  const getSubscriptionStatus = () => {
    if (!profileData.subscription_expires) {
      return { status: 'Free Plan', daysLeft: null, color: 'bg-gray-100 text-gray-800' };
    }

    const expiresDate = new Date(profileData.subscription_expires);
    const now = new Date();
    const daysLeft = Math.ceil((expiresDate - now) / (1000 * 60 * 60 * 24));

    if (daysLeft <= 0) {
      return { status: 'Expired', daysLeft: 0, color: 'bg-red-100 text-red-800' };
    } else if (daysLeft <= 7) {
      return { status: 'Expiring Soon', daysLeft, color: 'bg-yellow-100 text-yellow-800' };
    } else {
      return { status: 'Active', daysLeft, color: 'bg-green-100 text-green-800' };
    }
  };

  const subscriptionInfo = getSubscriptionStatus();

  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
      <Card className="w-full max-w-2xl bg-slate-800 border-slate-700 max-h-[90vh] overflow-y-auto">
        <CardHeader className="flex flex-row items-center justify-between border-b border-slate-700 pb-4">
          <div>
            <CardTitle className="text-white">User Profile</CardTitle>
            <CardDescription className="text-slate-400">Manage your account settings</CardDescription>
          </div>
          <Button variant="ghost" size="sm" onClick={onClose} className="text-slate-400 hover:text-white">
            <X className="h-5 w-5" />
          </Button>
        </CardHeader>

        <CardContent className="space-y-6 pt-6">
          {/* Avatar Section */}
          <div className="flex flex-col items-center space-y-4">
            <Avatar className="h-24 w-24">
              <AvatarImage src={avatarPreview} alt={profileData.username} />
              <AvatarFallback className="bg-blue-600 text-white text-2xl">
                {profileData.username?.charAt(0).toUpperCase() || 'U'}
              </AvatarFallback>
            </Avatar>
            
            <div className="flex gap-2">
              <Label htmlFor="avatar-upload" className="cursor-pointer">
                <Button variant="outline" size="sm" className="border-slate-600 text-slate-300 hover:bg-slate-700" asChild>
                  <span>
                    <Upload className="h-4 w-4 mr-2" />
                    Upload Photo
                  </span>
                </Button>
                <Input
                  id="avatar-upload"
                  type="file"
                  accept="image/*"
                  className="hidden"
                  onChange={handleAvatarChange}
                />
              </Label>
            </div>
          </div>

          {/* Subscription Info */}
          <div className="bg-slate-700/50 rounded-lg p-4 space-y-2">
            <div className="flex items-center justify-between">
              <span className="text-slate-300 text-sm">Subscription Plan</span>
              <Badge className="bg-blue-600 text-white">
                {profileData.subscription_plan?.toUpperCase() || 'FREE'}
              </Badge>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-slate-300 text-sm">Status</span>
              <Badge className={subscriptionInfo.color}>
                {subscriptionInfo.status}
              </Badge>
            </div>
            {subscriptionInfo.daysLeft !== null && subscriptionInfo.daysLeft > 0 && (
              <div className="flex items-center justify-between">
                <span className="text-slate-300 text-sm">Days Remaining</span>
                <span className="text-white font-semibold">{subscriptionInfo.daysLeft} days</span>
              </div>
            )}
          </div>

          {/* Profile Information */}
          <div className="space-y-4">
            <div className="space-y-2">
              <Label htmlFor="username" className="text-slate-300">
                <User className="h-4 w-4 inline mr-2" />
                Username
              </Label>
              <Input
                id="username"
                value={profileData.username}
                onChange={(e) => setProfileData({ ...profileData, username: e.target.value })}
                className="bg-slate-700 border-slate-600 text-white"
              />
            </div>

            <div className="space-y-2">
              <Label htmlFor="email" className="text-slate-300">
                <Mail className="h-4 w-4 inline mr-2" />
                Email
              </Label>
              <Input
                id="email"
                type="email"
                value={profileData.email}
                onChange={(e) => setProfileData({ ...profileData, email: e.target.value })}
                className="bg-slate-700 border-slate-600 text-white"
              />
            </div>

            <div className="space-y-2">
              <Label className="text-slate-300">
                <Shield className="h-4 w-4 inline mr-2" />
                Role
              </Label>
              <Input
                value={user?.role === 'main_admin' ? 'Main Administrator' : user?.role === 'admin' ? 'Administrator' : 'Member'}
                disabled
                className="bg-slate-700 border-slate-600 text-slate-400"
              />
            </div>
          </div>

          <Button 
            onClick={handleProfileUpdate} 
            disabled={loading}
            className="w-full bg-blue-600 hover:bg-blue-700 text-white"
          >
            <Save className="h-4 w-4 mr-2" />
            {loading ? 'Saving...' : 'Save Profile'}
          </Button>

          {/* Password Change Section */}
          <div className="border-t border-slate-700 pt-6 space-y-4">
            <div className="flex items-center justify-between">
              <div>
                <h3 className="text-white font-semibold">Change Password</h3>
                <p className="text-slate-400 text-sm">Update your account password</p>
              </div>
              <Button
                variant="outline"
                size="sm"
                onClick={() => setIsEditingPassword(!isEditingPassword)}
                className="border-slate-600 text-slate-300 hover:bg-slate-700"
              >
                <Key className="h-4 w-4 mr-2" />
                {isEditingPassword ? 'Cancel' : 'Change'}
              </Button>
            </div>

            {isEditingPassword && (
              <div className="space-y-4 bg-slate-700/30 p-4 rounded-lg">
                <div className="space-y-2">
                  <Label htmlFor="current-password" className="text-slate-300">Current Password</Label>
                  <Input
                    id="current-password"
                    type="password"
                    value={passwordData.current_password}
                    onChange={(e) => setPasswordData({ ...passwordData, current_password: e.target.value })}
                    className="bg-slate-700 border-slate-600 text-white"
                  />
                </div>

                <div className="space-y-2">
                  <Label htmlFor="new-password" className="text-slate-300">New Password</Label>
                  <Input
                    id="new-password"
                    type="password"
                    value={passwordData.new_password}
                    onChange={(e) => setPasswordData({ ...passwordData, new_password: e.target.value })}
                    className="bg-slate-700 border-slate-600 text-white"
                  />
                </div>

                <div className="space-y-2">
                  <Label htmlFor="confirm-password" className="text-slate-300">Confirm New Password</Label>
                  <Input
                    id="confirm-password"
                    type="password"
                    value={passwordData.confirm_password}
                    onChange={(e) => setPasswordData({ ...passwordData, confirm_password: e.target.value })}
                    className="bg-slate-700 border-slate-600 text-white"
                  />
                </div>

                <Button 
                  onClick={handlePasswordChange} 
                  disabled={loading}
                  className="w-full bg-blue-600 hover:bg-blue-700 text-white"
                >
                  {loading ? 'Changing...' : 'Update Password'}
                </Button>
              </div>
            )}
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

export default UserProfile;
