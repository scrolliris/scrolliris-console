<div class="sidebar">
  <% locked = cookie.get('carrell.sidebar') %>
  <%include file='aarau:templates/shared/_sidebar_navi.mako' args="locked=locked,"/>

  % if util.route_name == 'carrell.read':
  <div class="publication item">
    <div class="cover">COVER IMAGE</div>
    <h6 class="name">${publication.name}</h6>
    <p></p>
  </div>

  <hr>
  <h6 class="section-title">CHAPTERS</h6>

  <hr>
  <h6 class="section-title">HEADINGS</h6>

  <hr>

  <h6 class="section-title">PREFERENCES</h6>

  <hr>
  % endif

  <a class="item${' active' if util.route_name.startswith('carrell.bookmark') or util.route_name == 'carrell.top' else ''}" href="${req.route_path('carrell.top')}">Bookmarks</a>
  <a class="disabled item" href="#">Preferences</a>

  <hr class="divider">
  <h6 class="section-title">LEAVE CARRELL</h6>
  % if req.user.projects:
  <a class="item" href="${req.route_url('console.top')}">
    Console
    <span class="description">writing space</span>
  </a>
  % endif
  <a class="item" href="${req.route_url('top', subdomain=None)}">
    Publication Registry
    <span class="description">search & browse stats</span>
  </a>
</div>
