document.addEventListener("DOMContentLoaded", function () {
    const buttons = document.querySelectorAll(".tag-filter");
    const posts = document.querySelectorAll(".post-item");
    let selectedTags = new Set(); // Store selected tags
  
    // Function to update the post visibility
    function updatePosts() {
      if (selectedTags.size === 0) {
        // If no tags are selected, show all posts
        posts.forEach(post => post.style.display = "block");
        return;
      }
  
      // Otherwise, filter based on selected tags
      posts.forEach(post => {
        const postTags = post.dataset.tags.split(",");
        if ([...selectedTags].every(tag => postTags.includes(tag))) {
          post.style.display = "block";
        } else {
          post.style.display = "none";
        }
      });
    }

    function updateCounts() {
        const posts_active = [...document.querySelectorAll(".post-item")].filter(
            post => getComputedStyle(post).display !== "none"
          );
        const tagCounts = {};

        posts_active.forEach(post => {
            post.dataset.tags.split(",").forEach(tag => {
              tagCounts[tag] = (tagCounts[tag] || 0) + 1;
            });
          });

        // console.log(tagCounts)
        buttons.forEach(tagElement => {
            const tag = tagElement.dataset.tag;
            const countSpan = tagElement.querySelector(".tag-count");
            countSpan.textContent = tagCounts[tag] || 0;
          });
    }
  
    // Event listener for each button
    buttons.forEach(button => {
        console.log('hi');
      button.addEventListener("click", function (event) {
        event.preventDefault(); // Prevents navigation (optional)
        const tag = this.dataset.tag;
        // alert("Link clicked!" + tag);
  
        if (selectedTags.has(tag)) {
          selectedTags.delete(tag);
          this.classList.remove("active"); // Remove active state
        } else {
          selectedTags.add(tag);
          this.classList.add("active"); // Mark as active
        }
  
        updatePosts(); // Update post visibility
        updateCounts();
      });
    });
  
    // // "Show All" button to reset the selection
    // document.getElementById("show-all").addEventListener("click", function () {
    //   selectedTags.clear();
    //   buttons.forEach(btn => btn.classList.remove("active")); // Reset active state
    //   updatePosts();
    // });
  });