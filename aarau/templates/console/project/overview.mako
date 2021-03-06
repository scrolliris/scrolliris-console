<%namespace file='aarau:templates/macro/_flash_message.mako' import="render_notice"/>
<%namespace file='aarau:templates/macro/_title.mako' import="render_title"/>

<%inherit file='aarau:templates/console/_layout.mako'/>

<%block name='title'>${render_title(project.name)}</%block>

<%block name='breadcrumb'>
<div class="breadcrumb">
  <span class="divider">/</span>
  <a class="item" href="${req.route_path('console.top')}">Projects</a>
  <span class="divider">/</span>
  <a class="item" href="${req.route_url('console.project.overview', namespace=project.namespace)}">${project.name}</a>
  <span class="divider">/</span>
  <span class="item active">Overview</span>
</div>
</%block>

<%block name='sidebar'>
  <%include file='aarau:templates/console/project/_sidebar.mako'/>
</%block>

<%block name='footer'>
</%block>

<div id="project" class="content">
  <div class="grid">
    <div class="row">
      <div class="column-16">
        ${render_notice()}
      </div>
    </div>

    <div class="row">
      <div class="column-16">
        <h4>${project.name}</h4>

        <p class="description">${project.description}</p>
        <div class="dropdown-container">
          <a class="action" href="${req.route_path('console.site.new', namespace=project.namespace, _query={'type': 'publication'})}">New Publication</a>
          <input id="site_type" type="checkbox">
          <label for="site_type"></label>
          <div class="dropdown">
            <a class="item" href="${req.route_path('console.site.new', namespace=project.namespace, _query={'type': 'publication'})}">
              <h5 class="header">Hosted Publication</h5>
              <span class="description">You publication will be published on scrolliris.com.</span>
            </a>
            <a class="item" href="${req.route_path('console.site.new', namespace=project.namespace, _query={'type': 'application'})}">
              <h5 class="header">Integrated Publication</h5>
              <span class="description">Choose this if you want to integrate readability measurement into you existing site.</span>
            </a>
          </div>
        </div>
      </div>
    </div>

    <div class="row">
    % for site in sites:
    <div class="column-4 column-v-8 column-l-16">
      <div class="${site.type} flat site box">
        <a href="${req.route_path('console.site.overview', namespace=project.namespace, slug=site.slug)}"><h5 class="header">${util.truncate(site.instance.name, length=28)}</h5></a>
        <label class="${site.type} label">${'scrolliris.com' if site.type == 'publication' else site.domain}</label>
        <p class="text">${util.truncate(site.instance.description, length=64)}</p>
      </div>
    </div>
    % endfor
    </div>
  </div>
</div>
