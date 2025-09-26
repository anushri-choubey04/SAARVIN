//NavBar
    // Searchbar suggestions
    const searchBox = document.getElementById("searchBox");
    const suggestions = document.getElementById("suggestions");

    const data = ["Saree", "Lehenga", "Kurta", "Western Dress", "Party Wear", "Sherwani"];

    searchBox?.addEventListener("input", () => {
      let value = searchBox.value.toLowerCase();
      suggestions.innerHTML = "";
      if (value) {
        let filtered = data.filter(item => item.toLowerCase().includes(value));
        if (filtered.length) {
          suggestions.style.display = "block";
          filtered.forEach(item => {
            let div = document.createElement("div");
            div.textContent = item;
            div.onclick = () => {
              searchBox.value = item;
              suggestions.style.display = "none";
            };
            suggestions.appendChild(div);
          });
        } else {
          suggestions.style.display = "none";
        }
      } else {
        suggestions.style.display = "none";
      }
    });

    // Mobile menu toggle
    const hamburger = document.getElementById("hamburger");
    const mobileMenu = document.getElementById("mobileMenu");
    const closeMenu = document.getElementById("closeMenu");

    hamburger.addEventListener("click", () => {
      mobileMenu.classList.add("active");
    });
    closeMenu.addEventListener("click", () => {
      mobileMenu.classList.remove("active");
    });

    // Support dropdown
    document.getElementById("supportToggleBtn").addEventListener("click", () => {
      document.getElementById("supportItems").classList.toggle("active");
    });

// END OF NAVBAR





// Stories js code
//  Viewer with Swipe Up and Progress Bar
// This code creates a simple stories viewer with swipe up functionality and a progress bar.

const stories = [
    {
      id: 1,
      type: "form",
      username: "List Your Clothes",
      image: null,
      formLink: "HTML/ListingForm.html",
    },
    {
      id: 2,
      username: "Wedding Collection",
      profilePic:
        "https://images.unsplash.com/photo-1590874103328-eac38a683ce7?ixlib=rb-1.2.1&auto=format&fit=crop&w=1000&q=80",
      media: [
        {
          type: "image",
          url: "https://images.unsplash.com/photo-1591047139829-d91aecb6caea?ixlib=rb-1.2.1&auto=format&fit=crop&w=1000&q=80",
          caption: "Discover our latest bridal collection",
        },
      ],
      timestamp: "2h",
      hasSwipeUp: true,
    },
    {
      id: 3,
      username: "Men's Wear",
      profilePic:
        "https://images.unsplash.com/photo-1593030761757-71fae45fa0e7?w=150&h=150&fit=crop",
      media: [
        {
          type: "image",
          url: "https://images.unsplash.com/photo-1593030761757-71fae45fa0e7?w=1080&h=1920&fit=crop",
          caption: "Premium suits for every occasion",
        },
      ],
      timestamp: "3h",
    },
  ];
  
  let currentStoryIndex = 0;
  let currentMediaIndex = 0;
  let isPaused = false;
  let progressInterval;
  
  const storiesContainer = document.getElementById("storiesContainer");
  const modal = document.getElementById("listingForm");
  const overlay = document.getElementById("modalOverlay");
  const storyViewer = document.getElementById("story-viewer");
  const storiesStrip = document.getElementById("stories-strip");
  const profilePic = document.getElementById("profile-pic");
  const username = document.getElementById("username");
  const timestamp = document.getElementById("timestamp");
  const storyContent = document.getElementById("story-content");
  const caption = document.getElementById("caption");
  const swipeUp = document.getElementById("swipe-up");
  const progressBars = document.getElementById("progress-bars");
  
  
  function openModal() {
    modal.classList.remove("hidden");
    overlay.classList.remove("hidden");
  }
  
  function closeModal() {
    modal.classList.add("hidden");
    overlay.classList.add("hidden");
  }
  
  function createStoryIcons() {
    stories.forEach((story, index) => {
      const btn = document.createElement("button");
      btn.className = "flex flex-col items-center flex-shrink-0";
      btn.innerHTML = `
          <div class="w-16 h-16 rounded-full border-2 border-[#8D1C23] p-0.5 mb-1">
            <img src="${story.profilePic}" class="w-full h-full rounded-full object-cover" />
          </div>
          <span class="text-lg text-center whitespace-nowrap">${story.username}</span>
        `;
      btn.addEventListener("click", () => openViewer(index));
      storiesStrip.appendChild(btn);
    });
  }
  
  function openViewer(index) {
    currentStoryIndex = index;
    currentMediaIndex = 0;
    storyViewer.classList.remove("hidden");
    loadStory();
  }
  
  function closeViewer() {
    storyViewer.classList.add("hidden");
    clearInterval(progressInterval);
  }
  
  
  function loadStory() {
    const story = stories[currentStoryIndex];
    const media = story.media[currentMediaIndex];
  
    profilePic.src = story.profilePic;
    username.textContent = story.username;
    timestamp.textContent = story.timestamp;
    caption.textContent = media.caption || "";
    swipeUp.style.display = story.hasSwipeUp ? "flex" : "none";
  
    storyContent.innerHTML = `
        <img src="${media.url}" class="w-full h-full object-cover absolute inset-0" />
      `;
  
    loadProgressBar(story.media.length);
    startProgress();
  }
  
  function loadProgressBar(count) {
    progressBars.innerHTML = "";
    for (let i = 0; i < count; i++) {
      const bar = document.createElement("div");
      bar.className = "h-0.5 flex-1 bg-white/30 overflow-hidden";
      if (i === currentMediaIndex) {
        const fill = document.createElement("div");
        fill.className = "h-full bg-white";
        fill.id = "active-progress";
        fill.style.width = "0%";
        bar.appendChild(fill);
      }
      progressBars.appendChild(bar);
    }
  }
  
  function startProgress() {
    let progress = 0;
    clearInterval(progressInterval);
    const activeProgress = document.getElementById("active-progress");
  
    progressInterval = setInterval(() => {
      if (!isPaused) {
        progress += 1;
        if (activeProgress) activeProgress.style.width = `${progress}%`;
        if (progress >= 100) {
          nextMedia();
        }
      }
    }, 50);
  }
  
  function nextMedia() {
    const story = stories[currentStoryIndex];
    if (currentMediaIndex < story.media.length - 1) {
      currentMediaIndex++;
    } else if (currentStoryIndex < stories.length - 1) {
      currentStoryIndex++;
      currentMediaIndex = 0;
    } else {
      closeViewer();
      return;
    }
    loadStory();
  }
  
  function previousMedia() {
    if (currentMediaIndex > 0) {
      currentMediaIndex--;
    } else if (currentStoryIndex > 0) {
      currentStoryIndex--;
      currentMediaIndex = stories[currentStoryIndex].media.length - 1;
    }
    loadStory();
  }
      
  
  // Touch navigation
  storyContent.addEventListener("touchstart", (e) => {
    const x = e.touches[0].clientX;
    const width = storyContent.offsetWidth;
    if (x < width * 0.25) {
      previousMedia();
    } else if (x > width * 0.75) {
      nextMedia();
    }
  });
  
  // Long press to pause
  let touchTimer;
  storyContent.addEventListener("touchstart", () => {
    touchTimer = setTimeout(() => {
      isPaused = true;
    }, 200);
  });
  storyContent.addEventListener("touchend", () => {
    clearTimeout(touchTimer);
    isPaused = false;
  });
  
  createStoryIcons();
  
  //end of story js code



 //Category section js code
 const categories = [
        {
          id: "graduation",
          name: "GRADUATION / FAREWELL",
          icon: "🎓",
          count: "120+ Items",
          color: "bg-blue-50 text-blue-600",
        },
        {
          id: "office",
          name: "OFFICE EVENT",
          icon: "💼",
          count: "180+ Items",
          color: "bg-gray-50 text-gray-600",
        },
        {
          id: "party",
          name: "PARTY WEAR",
          icon: "🍷",
          count: "250+ Items",
          color: "bg-purple-50 text-purple-600",
        },
        {
          id: "ethnic",
          name: "ETHNIC WEAR",
          icon: "👗",
          count: "300+ Items",
          color: "bg-red-50 text-red-600",
        },
        {
          id: "prewedding",
          name: "PREWEDDING PHOTOSHOOT",
          icon: "📷",
          count: "150+ Items",
          color: "bg-pink-50 text-pink-600",
        },
        {
          id: "attending",
          name: "ATTENDING WEDDING",
          icon: "🎁",
          count: "200+ Items",
          color: "bg-yellow-50 text-yellow-600",
        },
        {
          id: "date",
          name: "DATE NIGHT",
          icon: "HTML/images/table.jpeg",
          count: "400+ Items",
          color: "bg-rose-50 text-rose-600",
          isImage: true,
        },
      ];

      const container = document.getElementById("categoriesContainer");

      categories.forEach((category) => {
        const button = document.createElement("button");
        button.className =
          "flex flex-col items-center group focus:outline-none ";
        
        button.onclick = () => {
          window.location.href = `/categories/${category.id}.html`;
        };

        const iconHTML = category.isImage
          ? `<img src="${category.icon}" alt="${category.name}" class="w-10 h-10 rounded-full object-cover" />`
          : `<span class="text-4xl">${category.icon}</span>`;

        button.innerHTML = `
      <div class="w-24 h-24 ${category.color} rounded-full flex items-center justify-center mb-5 transition-transform duration-300 hover:scale-110 hover:shadow-lg relative">
        
        ${iconHTML}
        
        
      </div>
      <div class="text-center max-w-[100px]">
        <h3 class="text-sm text-black font-semibold break-words">${category.name}</h3>
        <p class="text-xs text-gray-500 mt-1">${category.count}</p>
      </div>
    `;

        container.appendChild(button);
      });
  // End of Category section js code



 
  // Quick View js code
  const quickViewButton = document.getElementById("quickViewButton");
  const products = [
  {
    id: 1,
    brand: 'MAYKR',
    category: 'Smart Casual Wear',
    price: 599,
    image: 'Hero/gown1.png'
  },
  {
    id: 2,
    brand: 'ISHRANSH',
    category: "Women's Fancy Gown",
    price: 499,
    image: 'Hero/gown2.png'
  },
  {
    id: 3,
    brand: 'FIT & FLARE',
    category: 'Designer Dresses',
    price: 799,
    image: 'Hero/lehnga3.png'
  },
  {
    id: 4,
    brand: 'ETHNIC',
    category: 'Traditional Wear',
    price: 899,
    image: 'ProductSection/IMAGES/sherwani.jpeg'
  },
  {
    id: 5,
    brand: 'STYLE',
    category: 'Stylish Collection',
    price: 699,
    image: 'Hero/lehnga2.png'
  },
  {
    id: 6,
    brand: 'LUXE WEAR',
    category: 'Premium Fashion',
    price: 999,
    image: 'ProductSection/IMAGES/sherwani2.jpeg'
  },
  {
    id: 7,
    brand: 'WEAR',
    category: 'Premium',
    price: 999,
    image: 'ProductSection/IMAGES/tuexdo.jpeg'
  }
];

// Inject products
const productList = document.getElementById('product-list');

products.forEach(product => {
  const slide = document.createElement('div');
  slide.className = 'swiper-slide';
  slide.innerHTML = `
    <div class="product-image">
      <img src="${product.image}" alt="${product.brand}" />
    </div>
    <div class="product-info">
      <h3>${product.brand}</h3>
      <p>${product.category}</p>
      <p class="price">Under ₹${product.price}</p>
    </div>
  `;
  productList.appendChild(slide);
});

// Initialize Swiper
new Swiper('.swiper', {
  slidesPerView: 1.2,
  spaceBetween: 16,
  loop: true,
  autoplay: {
    delay: 2000,
    disableOnInteraction: false,
    pauseOnMouseEnter: true
  },
  pagination: {
    el: '.swiper-pagination',
    clickable: true,
    dynamicBullets: true
  },
  navigation: {
    nextEl: '.swiper-button-next',
    prevEl: '.swiper-button-prev'
  },
  breakpoints: {
    480: { slidesPerView: 1.5 },
    640: { slidesPerView: 2.2 },
    768: { slidesPerView: 2.5 },
    1024: { slidesPerView: 3.2 },
    1280: { slidesPerView: 4.2 }
  }
});
// End Quick View js code

//Video Section js code
const videos = Array.from(document.querySelectorAll(".auto-video"));
      function tryPlay(v) {
        const p = v.play();
        if (p && typeof p.catch === "function") p.catch(() => {});
      }
      function onEnter(v) {
        if (!v.src && v.dataset.src) v.src = v.dataset.src;
        tryPlay(v);
      }
      function onLeave(v) {
        if (!v.paused) v.pause();
      }

      if ("IntersectionObserver" in window) {
        const io = new IntersectionObserver(
          (entries) => {
            entries.forEach((entry) => {
              const v = entry.target;
              if (entry.isIntersecting) onEnter(v);
              else onLeave(v);
            });
          },
          { threshold: 0.25 }
        );
        videos.forEach((v) => io.observe(v));
      } else {
        videos.forEach((v) => {
          if (v.dataset.src) v.src = v.dataset.src;
          tryPlay(v);
        });
      }

      // Tap to toggle mute/unmute
      document.addEventListener("click", (e) => {
        const v = e.target.closest("video.auto-video");
        if (!v) return;
        v.muted = !v.muted;
        tryPlay(v);
      });

      // End of Video Section js code
      

  // Footer section js code
      document.querySelectorAll('.accordion-toggle').forEach(button => {
    button.addEventListener('click', () => {
      const content = button.nextElementSibling;
      const isActive = button.classList.contains('active');
  
      document.querySelectorAll('.accordion-toggle').forEach(btn => btn.classList.remove('active'));
      document.querySelectorAll('.accordion-content').forEach(content => content.style.display = 'none');
  
      if (!isActive) {
        button.classList.add('active');
        content.style.display = 'block';
      }
    });
  });
  // End of Footer section js code
    
  