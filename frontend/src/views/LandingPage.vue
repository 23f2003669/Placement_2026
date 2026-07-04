<template>
  <div>

    <!-- Navbar -->
    <nav
      class="navbar px-4 px-md-5 py-3"
      style="background: rgba(255,255,255,0.08);
             backdrop-filter: blur(10px);
             position: absolute;
             width: 100%;
             z-index: 10;"
    >
      <div class="d-flex align-items-center gap-2">
        <i class="bi bi-briefcase-fill text-white fs-5"></i>
        <span class="text-white fw-semibold">Placement Portal</span>
      </div>
      <div class="d-flex gap-2 ms-auto">
        <router-link to="/login" class="btn btn-outline-light btn-sm px-3">
          Login
        </router-link>
      </div>
    </nav>

    <!-- Hero -->
    <section
      style="background: linear-gradient(135deg, #0d6efd 0%, #6610f2 100%);
             min-height: 85vh;
             display: flex;
             align-items: center;
             padding: 120px 0 80px;
             position: relative;
             overflow: hidden;"
    >
      <!-- Background decoration circles -->
      <div style="position:absolute; top:-100px; right:-100px;
                  width:400px; height:400px; border-radius:50%;
                  background:rgba(255,255,255,0.05);"></div>
      <div style="position:absolute; bottom:-150px; left:-50px;
                  width:300px; height:300px; border-radius:50%;
                  background:rgba(255,255,255,0.04);"></div>

      <div class="container text-center text-white position-relative">

        <span
          class="badge mb-4 px-3 py-2"
          style="background:rgba(255,255,255,0.15);
                 font-size:12px; letter-spacing:2px;
                 text-transform:uppercase; border-radius:50px;"
        >
          Institute Placement Cell
        </span>

        <h1
          class="display-3 fw-bold mb-4"
          style="letter-spacing:-1px; line-height:1.1;"
        >
          Your Career Starts Here
        </h1>

        <p
          class="lead mb-5 mx-auto"
          style="opacity:0.88; max-width:560px; font-size:1.15rem;"
        >
          Connecting students with top recruiters through a modern
          campus placement platform — seamless, fast, and transparent.
        </p>

        <div class="d-flex gap-3 justify-content-center flex-wrap">
          <router-link
            to="/register"
            class="btn btn-light btn-lg px-5 fw-semibold"
            style="border-radius:50px; color:#0d6efd;"
          >
            <i class="bi bi-mortarboard-fill me-2"></i>
            Student register
          </router-link>
          <router-link
            to="/register-company"
            class="btn btn-lg px-5 fw-semibold"
            style="background:rgba(255,255,255,0.15);
                   color:white;
                   border:1.5px solid rgba(255,255,255,0.5);
                   border-radius:50px;"
          >
            <i class="bi bi-buildings-fill me-2"></i>
            Company register
          </router-link>
        </div>

        <!-- Stats overlapping hero bottom -->
        <div class="row g-3 mt-5 pt-3">
          <div class="col-6 col-md-3">
            <div
              class="p-3 rounded-3"
              style="background:rgba(255,255,255,0.12);
                     backdrop-filter:blur(10px);
                     border:1px solid rgba(255,255,255,0.2);"
            >
              <div class="fs-3 fw-bold">1200+</div>
              <div class="small" style="opacity:0.8;">Students placed</div>
            </div>
          </div>
          <div class="col-6 col-md-3">
            <div
              class="p-3 rounded-3"
              style="background:rgba(255,255,255,0.12);
                     backdrop-filter:blur(10px);
                     border:1px solid rgba(255,255,255,0.2);"
            >
              <div class="fs-3 fw-bold">150+</div>
              <div class="small" style="opacity:0.8;">Recruiters</div>
            </div>
          </div>
          <div class="col-6 col-md-3">
            <div
              class="p-3 rounded-3"
              style="background:rgba(255,255,255,0.12);
                     backdrop-filter:blur(10px);
                     border:1px solid rgba(255,255,255,0.2);"
            >
              <div class="fs-3 fw-bold">300+</div>
              <div class="small" style="opacity:0.8;">Active drives</div>
            </div>
          </div>
          <div class="col-6 col-md-3">
            <div
              class="p-3 rounded-3"
              style="background:rgba(255,255,255,0.12);
                     backdrop-filter:blur(10px);
                     border:1px solid rgba(255,255,255,0.2);"
            >
              <div class="fs-3 fw-bold">45 LPA</div>
              <div class="small" style="opacity:0.8;">Highest package</div>
            </div>
          </div>
        </div>

      </div>
    </section>

    <!-- Features -->
    <section class="py-5" style="background:#f8f9fa;">
      <div class="container py-3">

        <div class="text-center mb-5">
          <h2 class="fw-bold mb-2">Everything you need</h2>
          <p class="text-muted">One platform for students, companies, and placement cell</p>
        </div>

        <div class="row g-4 mb-5">

          <div class="col-md-4">
            <div class="card border-0 h-100 p-4"
              style="border-radius:16px; box-shadow:0 2px 20px rgba(0,0,0,0.06);">
              <div
                class="mb-3 d-inline-flex p-3 rounded-3"
                style="background:rgba(13,110,253,0.1);"
              >
                <i class="bi bi-mortarboard-fill text-primary fs-4"></i>
              </div>
              <h5 class="fw-semibold mb-3">For students</h5>
              <ul class="text-muted list-unstyled">
                <li class="mb-2">
                  <i class="bi bi-check-circle-fill text-primary me-2 small"></i>
                  Register and build your profile
                </li>
                <li class="mb-2">
                  <i class="bi bi-check-circle-fill text-primary me-2 small"></i>
                  Upload resume and apply for drives
                </li>
                <li class="mb-2">
                  <i class="bi bi-check-circle-fill text-primary me-2 small"></i>
                  Track application status live
                </li>
                <li class="mb-2">
                  <i class="bi bi-check-circle-fill text-primary me-2 small"></i>
                  View complete placement history
                </li>
              </ul>
            </div>
          </div>

          <div class="col-md-4">
            <div
              class="card border-0 h-100 p-4 text-white"
              style="border-radius:16px;
                     background:linear-gradient(135deg, #0d6efd, #6610f2);
                     box-shadow:0 8px 30px rgba(13,110,253,0.3);"
            >
              <div
                class="mb-3 d-inline-flex p-3 rounded-3"
                style="background:rgba(255,255,255,0.15);"
              >
                <i class="bi bi-buildings-fill fs-4"></i>
              </div>
              <h5 class="fw-semibold mb-3">For companies</h5>
              <ul class="list-unstyled" style="opacity:0.9;">
                <li class="mb-2">
                  <i class="bi bi-check-circle-fill me-2 small"></i>
                  Register and get admin approval
                </li>
                <li class="mb-2">
                  <i class="bi bi-check-circle-fill me-2 small"></i>
                  Post placement drives easily
                </li>
                <li class="mb-2">
                  <i class="bi bi-check-circle-fill me-2 small"></i>
                  Manage and shortlist applicants
                </li>
                <li class="mb-2">
                  <i class="bi bi-check-circle-fill me-2 small"></i>
                  Schedule interviews and select candidates
                </li>
              </ul>
            </div>
          </div>

          <div class="col-md-4">
            <div class="card border-0 h-100 p-4"
              style="border-radius:16px; box-shadow:0 2px 20px rgba(0,0,0,0.06);">
              <div
                class="mb-3 d-inline-flex p-3 rounded-3"
                style="background:rgba(255,193,7,0.1);"
              >
                <i class="bi bi-shield-check-fill text-warning fs-4"></i>
              </div>
              <h5 class="fw-semibold mb-3">Placement cell</h5>
              <ul class="text-muted list-unstyled">
                <li class="mb-2">
                  <i class="bi bi-check-circle-fill text-warning me-2 small"></i>
                  Approve companies and drives
                </li>
                <li class="mb-2">
                  <i class="bi bi-check-circle-fill text-warning me-2 small"></i>
                  Manage all students and companies
                </li>
                <li class="mb-2">
                  <i class="bi bi-check-circle-fill text-warning me-2 small"></i>
                  Monitor placements in real time
                </li>
                <li class="mb-2">
                  <i class="bi bi-check-circle-fill text-warning me-2 small"></i>
                  View statistics and reports
                </li>
              </ul>
            </div>
          </div>

        </div>

        <!-- Top Recruiters -->
        <div
          class="card border-0 p-4 p-md-5 text-center"
          style="border-radius:16px; box-shadow:0 2px 20px rgba(0,0,0,0.06);"
        >
          <h5 class="fw-semibold mb-1">Top recruiters</h5>
          <p class="text-muted small mb-4">Companies that trust our placement process</p>
          <div class="d-flex gap-3 justify-content-center flex-wrap">
            <span
              v-for="company in ['Google', 'Amazon', 'Microsoft', 'Infosys', 'TCS', 'Wipro']"
              :key="company"
              class="px-4 py-2 fw-semibold text-muted"
              style="background:#f1f3f5;
                     border-radius:50px;
                     font-size:14px;"
            >
              {{ company }}
            </span>
          </div>
        </div>

      </div>
    </section>

    <!-- CTA Section -->
    <section
      class="py-5 text-white text-center"
      style="background:linear-gradient(135deg, #0d6efd 0%, #6610f2 100%);"
    >
      <div class="container py-3">
        <h2 class="fw-bold mb-3">Ready to get placed?</h2>
        <p class="mb-4" style="opacity:0.88;">
          Join thousands of students already using the portal
        </p>
        <div class="d-flex gap-3 justify-content-center flex-wrap">
          <router-link
            to="/register"
            class="btn btn-light btn-lg px-5 fw-semibold"
            style="border-radius:50px; color:#0d6efd;"
          >
            Get started
          </router-link>
          <router-link
            to="/login"
            class="btn btn-outline-light btn-lg px-5"
            style="border-radius:50px;"
          >
            Login
          </router-link>
        </div>
      </div>
    </section>

    <!-- Footer -->
    <footer class="py-4 text-center" style="background:#1a1a2e;">
      <p class="text-muted small mb-0">
        Placement Portal — Built with Flask, Vue.js and Bootstrap
      </p>
    </footer>

  </div>
</template>

<script setup>
</script>