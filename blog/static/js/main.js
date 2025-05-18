// Wait for the DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips if Bootstrap is available
    if (typeof bootstrap !== 'undefined') {
        var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
        var tooltipList = tooltipTriggerList.map(function(tooltipTriggerEl) {
            return new bootstrap.Tooltip(tooltipTriggerEl);
        });
    }

    // Initialize toast functionality
    function showToast(message, type = 'info') {
        const toastContainer = document.getElementById('toast-container');
        if (!toastContainer) {
            // Create toast container if it doesn't exist
            const container = document.createElement('div');
            container.id = 'toast-container';
            container.className = 'position-fixed bottom-0 end-0 p-3';
            container.style.zIndex = '11';
            document.body.appendChild(container);
        }

        // Create toast element
        const toastId = 'toast-' + Date.now();
        const toast = document.createElement('div');
        toast.className = `toast align-items-center text-white bg-${type} border-0`;
        toast.id = toastId;
        toast.setAttribute('role', 'alert');
        toast.setAttribute('aria-live', 'assertive');
        toast.setAttribute('aria-atomic', 'true');

        // Create toast content
        toast.innerHTML = `
            <div class="d-flex">
                <div class="toast-body">
                    ${message}
                </div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
            </div>
        `;

        // Add toast to container
        document.getElementById('toast-container').appendChild(toast);

        // Initialize and show toast
        const bsToast = new bootstrap.Toast(toast);
        bsToast.show();

        // Remove toast after it's hidden
        toast.addEventListener('hidden.bs.toast', function() {
            this.remove();
        });
    }

    // Make toast function globally available
    window.showToast = showToast;

    // Scroll to top functionality
    const scrollToTopBtn = document.getElementById('scroll-to-top');
    if (scrollToTopBtn) {
        // Show/hide button based on scroll position
        window.addEventListener('scroll', function() {
            if (window.pageYOffset > 300) {
                scrollToTopBtn.style.display = 'flex';
            } else {
                scrollToTopBtn.style.display = 'none';
            }
        });

        // Scroll to top when button is clicked
        scrollToTopBtn.addEventListener('click', function() {
            window.scrollTo({
                top: 0,
                behavior: 'smooth'
            });
            showToast('Scrolled to top', 'info');
        });
    }

    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();

            const targetId = this.getAttribute('href');
            if (targetId === '#') return;

            const targetElement = document.querySelector(targetId);
            if (targetElement) {
                window.scrollTo({
                    top: targetElement.offsetTop,
                    behavior: 'smooth'
                });
            }
        });
    });

    // Form validation for contact form
    const contactForm = document.querySelector('#contact form');
    if (contactForm) {
        contactForm.addEventListener('submit', function(e) {
            e.preventDefault();

            // Simple validation
            let valid = true;
            const name = document.getElementById('name');
            const email = document.getElementById('email');
            const message = document.getElementById('message');

            if (!name.value.trim()) {
                valid = false;
                name.classList.add('is-invalid');
            } else {
                name.classList.remove('is-invalid');
            }

            if (!email.value.trim() || !email.value.includes('@')) {
                valid = false;
                email.classList.add('is-invalid');
            } else {
                email.classList.remove('is-invalid');
            }

            if (!message.value.trim()) {
                valid = false;
                message.classList.add('is-invalid');
            } else {
                message.classList.remove('is-invalid');
            }

            if (valid) {
                // Store in local storage
                const contactData = {
                    name: name.value,
                    email: email.value,
                    message: message.value,
                    timestamp: new Date().toISOString()
                };

                // Get existing messages or initialize empty array
                const existingMessages = JSON.parse(localStorage.getItem('contactMessages') || '[]');
                existingMessages.push(contactData);
                localStorage.setItem('contactMessages', JSON.stringify(existingMessages));

                alert('Thank you for your message! We will get back to you soon.');
                contactForm.reset();
            }
        });
    }

    // User Signup Form
    const signupForm = document.getElementById('signup-form');
    if (signupForm) {
        signupForm.addEventListener('submit', function(e) {
            e.preventDefault();

            // Validate form
            let valid = true;
            const username = document.getElementById('id_username');
            const email = document.getElementById('id_email');
            const password = document.getElementById('id_password');
            const confirmPassword = document.getElementById('id_confirm_password');

            if (!username.value.trim()) {
                valid = false;
                username.classList.add('is-invalid');
            } else {
                username.classList.remove('is-invalid');
            }

            if (!email.value.trim() || !email.value.includes('@')) {
                valid = false;
                email.classList.add('is-invalid');
            } else {
                email.classList.remove('is-invalid');
            }

            if (!password.value) {
                valid = false;
                password.classList.add('is-invalid');
            } else {
                password.classList.remove('is-invalid');
            }

            if (password.value !== confirmPassword.value) {
                valid = false;
                confirmPassword.classList.add('is-invalid');
                document.getElementById('password-mismatch').style.display = 'block';
            } else {
                confirmPassword.classList.remove('is-invalid');
                document.getElementById('password-mismatch').style.display = 'none';
            }

            if (valid) {
                // Get agreement checkboxes
                const agreeTerms = document.getElementById('id_agree_terms');
                const receiveMarketing = document.getElementById('id_receive_marketing');

                // Check if terms are agreed to
                if (!agreeTerms || !agreeTerms.checked) {
                    const signupError = document.getElementById('signup-error');
                    signupError.textContent = 'You must agree to the Terms and Conditions and Privacy Policy to sign up.';
                    signupError.style.display = 'block';
                    return;
                }

                // Prepare data for fetch request
                const userData = {
                    username: username.value,
                    email: email.value,
                    password: password.value,
                    agree_terms: agreeTerms ? agreeTerms.checked : false,
                    receive_marketing: receiveMarketing ? receiveMarketing.checked : false
                };

                // Store in local storage
                localStorage.setItem('currentUser', JSON.stringify(userData));

                // Send fetch request
                fetch('/signup/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': getCsrfToken()
                    },
                    body: JSON.stringify(userData)
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        const signupSuccess = document.getElementById('signup-success');
                        signupSuccess.textContent = data.message;
                        signupSuccess.style.display = 'block';
                        signupForm.reset();

                        // Hide signup form and show ad campaign form
                        document.getElementById('signup-container').style.display = 'none';
                        document.getElementById('ad-campaign-container').style.display = 'block';
                    } else {
                        const signupError = document.getElementById('signup-error');
                        signupError.textContent = data.message;
                        signupError.style.display = 'block';
                    }
                })
                .catch(error => {
                    const signupError = document.getElementById('signup-error');
                    signupError.textContent = 'An error occurred. Please try again.';
                    signupError.style.display = 'block';
                });
            }
        });
    }

    // Ad Campaign Upload Form
    const adCampaignForm = document.getElementById('ad-campaign-form');
    if (adCampaignForm) {
        adCampaignForm.addEventListener('submit', function(e) {
            e.preventDefault();

            // Validate form
            let valid = true;
            const title = document.getElementById('id_title');
            const description = document.getElementById('id_description');
            const video = document.getElementById('id_video');
            const genre = document.getElementById('id_genre');
            const mood = document.getElementById('id_mood');
            const targetAudience = document.getElementById('id_target_audience');

            if (!title.value.trim()) {
                valid = false;
                title.classList.add('is-invalid');
            } else {
                title.classList.remove('is-invalid');
            }

            if (!description.value.trim()) {
                valid = false;
                description.classList.add('is-invalid');
            } else {
                description.classList.remove('is-invalid');
            }

            if (video.files.length === 0) {
                valid = false;
                video.classList.add('is-invalid');
            } else {
                video.classList.remove('is-invalid');
            }

            if (!genre.value) {
                valid = false;
                genre.classList.add('is-invalid');
            } else {
                genre.classList.remove('is-invalid');
            }

            if (!mood.value) {
                valid = false;
                mood.classList.add('is-invalid');
            } else {
                mood.classList.remove('is-invalid');
            }

            if (!targetAudience.value) {
                valid = false;
                targetAudience.classList.add('is-invalid');
            } else {
                targetAudience.classList.remove('is-invalid');
            }

            if (valid) {
                // For demo purposes, we'll use a placeholder video URL
                // In a real app, you would upload the video file to a server
                const videoUrl = 'https://picsum.photos/640/360';

                // Get current user from local storage
                const currentUser = JSON.parse(localStorage.getItem('currentUser') || '{}');

                // Prepare data for fetch request
                const campaignData = {
                    title: title.value,
                    description: description.value,
                    video_url: videoUrl,
                    genre: genre.value,
                    mood: mood.value,
                    target_audience: targetAudience.value,
                    username: currentUser.username || 'demo_user'
                };

                // Store in local storage
                const existingCampaigns = JSON.parse(localStorage.getItem('adCampaigns') || '[]');
                existingCampaigns.push({
                    ...campaignData,
                    timestamp: new Date().toISOString()
                });
                localStorage.setItem('adCampaigns', JSON.stringify(existingCampaigns));

                // Send fetch request
                fetch('/upload-ad-campaign/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': getCsrfToken()
                    },
                    body: JSON.stringify(campaignData)
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        const adCampaignSuccess = document.getElementById('ad-campaign-success');
                        adCampaignSuccess.textContent = data.message;
                        adCampaignSuccess.style.display = 'block';
                        adCampaignForm.reset();
                    } else {
                        const adCampaignError = document.getElementById('ad-campaign-error');
                        adCampaignError.textContent = data.message;
                        adCampaignError.style.display = 'block';
                    }
                })
                .catch(error => {
                    const adCampaignError = document.getElementById('ad-campaign-error');
                    adCampaignError.textContent = 'An error occurred. Please try again.';
                    adCampaignError.style.display = 'block';
                });
            }
        });
    }

    // Search Functionality
    const searchForm = document.getElementById('search-form');
    const searchResults = document.getElementById('search-results');

    if (searchForm && searchResults) {
        searchForm.addEventListener('submit', function(e) {
            e.preventDefault();

            const query = document.getElementById('search-input').value.trim();
            if (!query) return;

            // Show loading indicator
            searchResults.innerHTML = '<div class="text-center"><div class="spinner-border" role="status"><span class="visually-hidden">Loading...</span></div></div>';

            // Send fetch request
            fetch(`/search/?q=${encodeURIComponent(query)}`)
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        // Clear previous results
                        searchResults.innerHTML = '';

                        const results = data.results;
                        let resultsHtml = '';

                        // Artists
                        if (results.artists.length > 0) {
                            resultsHtml += '<h3>Artists</h3><div class="row">';
                            results.artists.forEach(function(artist) {
                                resultsHtml += `
                                    <div class="col-md-4 mb-3">
                                        <div class="card">
                                            <img src="${artist.image_url}" class="card-img-top" alt="${artist.name}">
                                            <div class="card-body">
                                                <h5 class="card-title">${artist.name}</h5>
                                            </div>
                                        </div>
                                    </div>
                                `;
                            });
                            resultsHtml += '</div>';
                        }

                        // Albums
                        if (results.albums.length > 0) {
                            resultsHtml += '<h3>Albums</h3><div class="row">';
                            results.albums.forEach(function(album) {
                                resultsHtml += `
                                    <div class="col-md-4 mb-3">
                                        <div class="card">
                                            <img src="${album.cover_image_url}" class="card-img-top" alt="${album.title}">
                                            <div class="card-body">
                                                <h5 class="card-title">${album.title}</h5>
                                                <p class="card-text">${album.artist__name}</p>
                                            </div>
                                        </div>
                                    </div>
                                `;
                            });
                            resultsHtml += '</div>';
                        }

                        // Tracks
                        if (results.tracks.length > 0) {
                            resultsHtml += '<h3>Tracks</h3><div class="list-group mb-4">';
                            results.tracks.forEach(function(track) {
                                resultsHtml += `
                                    <a href="#" class="list-group-item list-group-item-action">
                                        <div class="d-flex w-100 justify-content-between">
                                            <h5 class="mb-1">${track.title}</h5>
                                        </div>
                                        <p class="mb-1">${track.artist__name} - ${track.album__title}</p>
                                    </a>
                                `;
                            });
                            resultsHtml += '</div>';
                        }

                        // Ad Campaigns
                        if (results.ad_campaigns.length > 0) {
                            resultsHtml += '<h3>Ad Campaigns</h3><div class="row">';
                            results.ad_campaigns.forEach(function(campaign) {
                                resultsHtml += `
                                    <div class="col-md-6 mb-3">
                                        <div class="card">
                                            <div class="ratio ratio-16x9">
                                                <img src="${campaign.video_url}" class="card-img-top" alt="${campaign.title}">
                                            </div>
                                            <div class="card-body">
                                                <h5 class="card-title">${campaign.title}</h5>
                                                <p class="card-text">${campaign.description}</p>
                                                <span class="badge bg-primary">${campaign.mood}</span>
                                            </div>
                                        </div>
                                    </div>
                                `;
                            });
                            resultsHtml += '</div>';
                        }

                        if (resultsHtml === '') {
                            resultsHtml = '<div class="alert alert-info">No results found for "' + query + '"</div>';
                        }

                        searchResults.innerHTML = resultsHtml;
                    } else {
                        searchResults.innerHTML = '<div class="alert alert-danger">' + data.message + '</div>';
                    }
                })
                .catch(error => {
                    searchResults.innerHTML = '<div class="alert alert-danger">An error occurred. Please try again.</div>';
                });
        });
    }

    // Music player functionality
    initMusicPlayer();

    // Filtering functionality
    initFiltering();

    // Helper function to get CSRF token
    function getCsrfToken() {
        const cookieValue = document.cookie
            .split('; ')
            .find(row => row.startsWith('csrftoken='))
            ?.split('=')[1];
        return cookieValue || '';
    }

    // Initialize music player
    function initMusicPlayer() {
        const audioPlayer = document.getElementById('audio-player');
        if (!audioPlayer) return;

        const currentTrackTitle = document.getElementById('current-track-title');
        const currentTrackArtist = document.getElementById('current-track-artist');
        const currentTrackAlbum = document.getElementById('current-track-album');

        // Function to play a track and update play count
        function playTrack(audioSrc, title, artist, album, trackId) {
            // Update the audio player
            audioPlayer.src = audioSrc;
            audioPlayer.load();
            audioPlayer.play();

            // Update the now playing information
            currentTrackTitle.textContent = title;
            currentTrackArtist.textContent = artist;
            currentTrackAlbum.textContent = album;

            // Show toast notification
            showToast(`Now playing: ${title} by ${artist}`, 'success');

            // Update play count if trackId is provided
            if (trackId) {
                fetch(`/update-play-count/${trackId}/`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': getCsrfToken()
                    }
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        console.log(`Play count updated for track ${trackId}`);
                    }
                })
                .catch(error => {
                    console.error('Error updating play count:', error);
                });
            }
        }

        // Add click event to all play buttons
        document.querySelectorAll('.play-btn').forEach(button => {
            button.addEventListener('click', function() {
                const trackRow = this.closest('.track-row');
                const audioSrc = trackRow.dataset.audio;
                const title = trackRow.dataset.title;
                const artist = trackRow.dataset.artist;
                const album = trackRow.dataset.album;
                const trackId = trackRow.dataset.id;

                playTrack(audioSrc, title, artist, album, trackId);
            });
        });

        // Add click event to trending tracks
        document.querySelectorAll('.trending-track').forEach(track => {
            track.addEventListener('click', function(e) {
                e.preventDefault();
                const audioSrc = this.dataset.audio;
                const title = this.dataset.title;
                const artist = this.dataset.artist;
                const album = this.dataset.album;
                const trackId = this.dataset.id;

                playTrack(audioSrc, title, artist, album, trackId);
            });
        });

        // Add search results container after the search form
        const searchFormInMusic = document.querySelector('#music-player #search-form');
        if (searchFormInMusic && !document.querySelector('#music-player #search-results')) {
            const searchResults = document.createElement('div');
            searchResults.id = 'search-results';
            searchResults.className = 'mt-3';
            searchFormInMusic.parentNode.insertBefore(searchResults, searchFormInMusic.nextSibling);
        }
    }

    // Pexels API Integration for Artist Images
    function loadPexelsImages(query = 'musician') {
        fetch(`/pexels-images/?q=${encodeURIComponent(query)}`)
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    const images = data.images;
                    const artistImageContainers = document.querySelectorAll('.artist-image-container');

                    // Update artist images if containers exist
                    if (artistImageContainers.length > 0) {
                        artistImageContainers.forEach((container, index) => {
                            if (index < images.length) {
                                container.querySelector('img').src = images[index];
                            }
                        });
                    }
                }
            })
            .catch(error => {
                console.error('Error loading Pexels images:', error);
            });
    }

    // Load Pexels images when page loads
    loadPexelsImages();

    // Initialize filtering functionality
    function initFiltering() {
        // Current filter state
        let currentFilters = {
            genre: 'all',
            artist: 'all'
        };

        // Genre filtering
        document.querySelectorAll('.genre-filter').forEach(link => {
            link.addEventListener('click', function(e) {
                e.preventDefault();
                const genre = this.getAttribute('data-genre');
                currentFilters.genre = genre;
                applyFilters();
                showToast(`Filtered by genre: ${genre}`, 'info');

                // Update active state
                document.querySelectorAll('.genre-filter').forEach(el => {
                    el.classList.remove('fw-bold', 'text-primary');
                });
                this.classList.add('fw-bold', 'text-primary');
            });
        });

        // Artist filtering
        document.querySelectorAll('.artist-filter').forEach(link => {
            link.addEventListener('click', function(e) {
                e.preventDefault();
                const artist = this.getAttribute('data-artist');
                currentFilters.artist = artist;
                applyFilters();
                showToast(`Filtered by artist: ${artist}`, 'info');

                // Update active state
                document.querySelectorAll('.artist-filter').forEach(el => {
                    el.classList.remove('fw-bold', 'text-primary');
                });
                this.classList.add('fw-bold', 'text-primary');
            });
        });

        // Genre badge filtering
        document.querySelectorAll('.genre-badge').forEach(badge => {
            badge.style.cursor = 'pointer';
            badge.addEventListener('click', function(e) {
                e.preventDefault();
                const genre = this.getAttribute('data-genre');
                currentFilters.genre = genre;
                applyFilters();
                showToast(`Filtered by genre: ${genre}`, 'info');

                // Update active state
                document.querySelectorAll('.genre-filter').forEach(el => {
                    el.classList.remove('fw-bold', 'text-primary');
                    if (el.getAttribute('data-genre') === genre) {
                        el.classList.add('fw-bold', 'text-primary');
                    }
                });
            });
        });

        // Apply filters to albums and tracks
        function applyFilters() {
            // Filter albums
            document.querySelectorAll('.album-item').forEach(album => {
                const albumArtist = album.getAttribute('data-artist');
                const albumGenres = album.getAttribute('data-genres').split(',');

                let showAlbum = true;

                // Apply artist filter
                if (currentFilters.artist !== 'all' && albumArtist !== currentFilters.artist) {
                    showAlbum = false;
                }

                // Apply genre filter
                if (currentFilters.genre !== 'all' && !albumGenres.includes(currentFilters.genre)) {
                    showAlbum = false;
                }

                // Show/hide album
                album.style.display = showAlbum ? '' : 'none';
            });

            // Filter tracks
            document.querySelectorAll('.track-row').forEach(track => {
                const trackArtist = track.getAttribute('data-artist');
                const trackGenres = track.getAttribute('data-genres').split(',');

                let showTrack = true;

                // Apply artist filter
                if (currentFilters.artist !== 'all' && trackArtist !== currentFilters.artist) {
                    showTrack = false;
                }

                // Apply genre filter
                if (currentFilters.genre !== 'all' && !trackGenres.includes(currentFilters.genre)) {
                    showTrack = false;
                }

                // Show/hide track
                track.style.display = showTrack ? '' : 'none';
            });
        }
    }
});
