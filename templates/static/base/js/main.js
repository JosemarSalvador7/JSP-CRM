(function() {
      // Inicializar tooltips
      const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]');
      const tooltips = [...tooltipTriggerList].map(el => new bootstrap.Tooltip(el, {
        delay: { show: 200, hide: 100 },
        trigger: 'hover focus'
      }));

      // Elementos do sidebar
      const sidebar = document.getElementById('dashboardSidebar');
      const mainWrapper = document.getElementById('mainWrapper');
      const sidebarToggle = document.getElementById('sidebarToggle');
      const mobileMenuBtn = document.getElementById('mobileMenuBtn');
      const sidebarOverlay = document.getElementById('sidebarOverlay');

      // Alternar sidebar expandir/recolher
      function toggleSidebar() {
        if (window.innerWidth > 992) {
          sidebar.classList.toggle('collapsed');
          mainWrapper.classList.toggle('expanded');
          
          const icon = sidebarToggle.querySelector('i');
          if (sidebar.classList.contains('collapsed')) {
            icon.classList.remove('fa-chevron-left');
            icon.classList.add('fa-chevron-right');
          } else {
            icon.classList.remove('fa-chevron-right');
            icon.classList.add('fa-chevron-left');
          }
          
          tooltips.forEach(t => t.dispose());
          setTimeout(() => {
            document.querySelectorAll('[data-bs-toggle="tooltip"]').forEach(el => {
              new bootstrap.Tooltip(el, { delay: { show: 200, hide: 100 } });
            });
          }, 100);
        }
      }

      // Alternar menu mobile
      function toggleMobileMenu() {
        sidebar.classList.toggle('mobile-open');
        sidebarOverlay.classList.toggle('active');
        document.body.style.overflow = sidebar.classList.contains('mobile-open') ? 'hidden' : '';
      }

      // Fechar menu mobile
      function closeMobileMenu() {
        sidebar.classList.remove('mobile-open');
        sidebarOverlay.classList.remove('active');
        document.body.style.overflow = '';
      }

      // Lidar com redimensionamento
      function handleResize() {
        if (window.innerWidth <= 992 && window.innerWidth > 768) {
          sidebar.classList.add('collapsed');
          mainWrapper.classList.add('expanded');
          sidebar.classList.remove('mobile-open');
          sidebarOverlay.classList.remove('active');
        } else if (window.innerWidth <= 768) {
          sidebar.classList.remove('collapsed');
          mainWrapper.classList.remove('expanded');
        } else {
          sidebar.classList.remove('mobile-open');
          sidebarOverlay.classList.remove('active');
          document.body.style.overflow = '';
        }
      }

      // Event listeners
      if (sidebarToggle) sidebarToggle.addEventListener('click', toggleSidebar);
      if (mobileMenuBtn) mobileMenuBtn.addEventListener('click', toggleMobileMenu);
      if (sidebarOverlay) sidebarOverlay.addEventListener('click', closeMobileMenu);

      document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && sidebar.classList.contains('mobile-open')) {
          closeMobileMenu();
        }
      });

      window.addEventListener('resize', handleResize);
      handleResize();

      // Estado ativo na navegação
      const navLinks = document.querySelectorAll('.nav-link-custom');
      navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
          if (window.innerWidth <= 768) {
            closeMobileMenu();
          }
        });
      });

     
    })();