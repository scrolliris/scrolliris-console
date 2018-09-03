<div class="sidebar">
  <% locked = cookie.get('console.sidebar') %>
  <%include file='aarau:templates/shared/_sidebar_navi.mako' args="locked=locked,"/>

  <span class="item active expanded">
    <%def name="link_to(route_name, text, default_link=False)">
      %if (util.route_name == route_name) or default_link:
        <a class="active item" href="${req.route_url(route_name, namespace=project.namespace)}">${text}</a>
      %else:
        <a class="item" href="${req.route_url(route_name, namespace=project.namespace)}">${text}</a>
      %endif
    </%def>

    <span class="item">Overview</span>
    <span class="item-container">
      ${link_to('console.project.overview', 'Publications', default_link=True)}
      <a class="disabled item">Activities</a>
    </span>
  </span>
  <a class="disabled item">Members</a>
  <a class="disabled item">Settings</a>

  <hr class="divider">
  <%include file='aarau:templates/shared/_sidebar_bottom_console.mako' />

  ## desktop only
  <div class="bottom note item">
    <%include file='aarau:templates/console/_sidebar_note.mako'/>
  </div>
</div>
