<template>
  <div class="profile-container">
    <!-- Current User Profile -->
    <div class="profile-header">
      <div class="image-placeholder">
        <img
          v-if="profile.profile_picture"
          :src="profile.profile_picture"
          :key="profile.profile_picture"
          alt="Profile Picture"
        />
        <span v-else>No Image</span>
      </div>
      <div class="info">
        <h2>{{ profile.name }}</h2>
        <p><strong>Branch:</strong> {{ profile.branch }}</p>
        <p><strong>Year:</strong> {{ profile.year }}</p>
        <p><strong>Skills:</strong> {{ profile.skills }}</p>
        <p><strong>About:</strong> {{ profile.About }}</p>
        <button @click="editing = true" class="btn btn-edit">Edit Profile</button>
      </div>
    </div>

    <div v-if="editing" class="edit-form">
      <input v-model="profile.name" placeholder="Name" />
      <input v-model="profile.branch" placeholder="Branch" />
      <input v-model="profile.year" placeholder="Year" />
      <input v-model="profile.skills" placeholder="Skills" />
      <input v-model="profile.About" placeholder="About" />

      <!-- Profile Picture Upload -->
      <div class="upload-section">
        <input type="file" @change="onFileChange" />
        <img v-if="previewUrl" :src="previewUrl" class="preview-img" />
        <button @click="uploadPicture" class="btn btn-upload">Upload Picture</button>
      </div>

      <button @click="updateProfile" class="btn btn-save">Save</button>
    </div>

    <!-- Search Bar -->
    <div class="search-section">
      <h3 class="section-title">Search Profiles</h3>
      <input
        v-model="searchQuery"
        @input="filterProfiles"
        placeholder="Search by name, branch, year or skills..."
        class="search-bar"
      />
      <div v-if="filteredProfiles.length > 0" class="search-results">
        <div v-for="p in filteredProfiles" :key="p.id" class="profile-card">
          <h4>{{ p.name }}</h4>
          <p><strong>Branch:</strong> {{ p.branch }}</p>
          <p><strong>Year:</strong> {{ p.year }}</p>
          <p><strong>Skills:</strong> {{ p.skills }}</p>
          <p><strong>About:</strong> {{ p.About }}</p>
        </div>
      </div>
      <div v-else-if="searchQuery.trim()" class="no-results">No profiles found.</div>
    </div>

    
  </div>
</template>

<script>

export default {
  
  data() {
    return {
      profile: {},
      editing: false,
      searchQuery: '',
      allProfiles: [],
      filteredProfiles: [],
      selectedFile: null,
      previewUrl: null
    };
  },
  methods: {
    async fetchProfile() {
      try {
        const response = await fetch('/profile/profile/me', {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`
          }
        });
        if (!response.ok) throw new Error('Failed to fetch profile');
        const data = await response.json();
        this.profile = data;
      } catch (error) {
        console.error(error);
      }
    },
    async updateProfile() {
      try {
        const response = await fetch('/profile/profile/me', {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${localStorage.getItem('token')}`
          },
          body: JSON.stringify(this.profile)
        });
        if (!response.ok) throw new Error('Failed to update profile');
        this.editing = false;
        await this.fetchProfile(); // refresh after update
        alert('Profile updated successfully.');
      } catch (error) {
        console.error(error);
        alert('Error updating profile.');
      }
    },
    async fetchAllProfiles() {
      try {
        const response = await fetch('/profile/profiles', {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`
          }
        });
        if (!response.ok) throw new Error('Failed to fetch profiles');
        const data = await response.json();
        this.allProfiles = data;
        this.filteredProfiles = data;
      } catch (error) {
        console.error('Error fetching all profiles:', error);
      }
    },
    filterProfiles() {
      const query = this.searchQuery.toLowerCase();
      this.filteredProfiles = this.allProfiles.filter(p =>
        p.name.toLowerCase().includes(query) ||
        p.branch.toLowerCase().includes(query) ||
        p.year.toLowerCase().includes(query) ||
        p.skills.toLowerCase().includes(query)
      );
    },
    onFileChange(event) {
      const file = event.target.files[0];
      if (file) {
        this.selectedFile = file;
        this.previewUrl = URL.createObjectURL(file);
      }
    },
    async uploadPicture() {
      if (!this.selectedFile) {
        alert('Please select a file first.');
        return;
      }

      const formData = new FormData();
      formData.append('picture', this.selectedFile);

      try {
        const response = await fetch('/profile/upload-profile-picture', {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`
          },
          body: formData
        });

        if (!response.ok) throw new Error('Failed to upload picture');
        alert('Profile picture updated!');
        this.previewUrl = null;
        this.selectedFile = null;

        await this.fetchProfile(); // ✅ reload profile with new image URL
      } catch (error) {
        console.error(error);
        alert('Error uploading profile picture.');
      }
    }
  },
  mounted() {
    this.fetchProfile();
    this.fetchAllProfiles();
  }
};
</script>

<style scoped>
.profile-container {
  max-width: 900px;
  margin: 0 auto;
  padding: 30px;
  font-family: 'Segoe UI', sans-serif;
}
.profile-header {
  display: flex;
  align-items: center;
  gap: 20px;
  margin-bottom: 30px;
  border-bottom: 1px solid #ddd;
  padding-bottom: 20px;
}
.image-placeholder {
  width: 100px;
  height: 100px;
  background: #eee;
  border-radius: 50%;
  overflow: hidden;
  display: flex;
  justify-content: center;
  align-items: center;
}
.image-placeholder img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}
.info h2 {
  margin: 0;
  font-size: 28px;
  color: #2c3e50;
}
.info p {
  margin: 5px 0;
  color: #555;
}
.btn {
  margin-top: 10px;
  padding: 8px 14px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}
.btn-edit {
  background-color: #0073b1;
  color: white;
}
.btn-save {
  background-color: #28a745;
  color: white;
}
.btn-upload {
  background-color: #ffa500;
  color: white;
  margin-top: 10px;
}
.edit-form input {
  display: block;
  width: 100%;
  padding: 8px;
  margin-top: 10px;
  margin-bottom: 5px;
  border: 1px solid #ccc;
  border-radius: 5px;
}
.upload-section {
  margin-top: 10px;
}
.preview-img {
  width: 100px;
  height: 100px;
  object-fit: cover;
  border-radius: 50%;
  margin-top: 10px;
}
.section-title {
  font-size: 22px;
  margin-top: 40px;
  margin-bottom: 15px;
  color: #2c3e50;
  border-bottom: 2px solid #0073b1;
  padding-bottom: 5px;
}
.search-section {
  margin-top: 20px;
}
.search-bar {
  width: 100%;
  padding: 10px;
  margin-bottom: 15px;
  border-radius: 6px;
  border: 1px solid #bbb;
  font-size: 16px;
}
.search-results {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 15px;
}
.profile-card {
  background-color: #f7f7f7;
  border: 1px solid #ddd;
  padding: 15px;
  border-radius: 10px;
  transition: 0.3s;
}
.profile-card:hover {
  background-color: #eef6fb;
  border-color: #0073b1;
}
.profile-card h4 {
  margin: 0 0 5px;
  color: #0073b1;
}
.no-results {
  color: #999;
  font-style: italic;
  padding: 10px 0;
}
</style>
