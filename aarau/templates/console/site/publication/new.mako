<%namespace file='aarau:templates/macro/_flash_message.mako' import="render_notice"/>
<%namespace file='aarau:templates/macro/_title.mako' import="render_title"/>

<%inherit file='aarau:templates/console/_layout.mako'/>

<%block name='title'>${render_title('{:s} - {:s}'.format(_('title.publication.new'), project.name))}</%block>
<%block name='body_attr'> data-locale-file="${req.util.static_url('{}')|unquote,formatting('locale/{{lng}}/{{ns}}.json'),h}"</%block>

<%block name='breadcrumb'>
<div class="breadcrumb">
  <span class="divider">/</span>
  <%include file='aarau:templates/console/site/publication/_breadcrumb_parent_items.mako'/>
  <span class="active item">New Publication</span>
</div>
</%block>

<%block name='sidebar'>
<div class="sidebar">
  <% locked = cookie.get('console.sidebar') %>
  <%include file='aarau:templates/shared/_sidebar_navi.mako' args="locked=locked,"/>
  <a class="item active">New Publication</a>

  <hr class="divider">
  <%include file='aarau:templates/shared/_sidebar_bottom_console.mako' />
</div>
</%block>

<div id="publication" class="content">
  <div class="grid">
    <div class="row">
      <div class="column-16">
        ${render_notice()}
      </div>
    </div>

    <div class="row">
      <div class="column-16">
        <form id="site" class="form" action="" method="get">
          <div class="field-6">
            <select id="site_type">
              <option value="publication" selected>Hosted on Scrolliris.com</option>
              <option value="application">Integration to Your Site</option>
            </select>
          </div>
        </form>
      </div>

      <div class="container column-16">
        <div class="attached header">
          <h5>New Publication</h5>
        </div>

        <div class="attached box">
          <p class="description">Create new publication which is published on Scrolliris.</p>
          <%
            act = req.route_url('console.site.new', namespace=project.namespace, _query={'type':'publication'})
            ctx = 'new'
            err = form.errors
            obj = site
          %>
          <%include file="aarau:templates/console/site/publication/_form.mako" args="f=form, act=act, ctx=ctx, err=err, obj=obj"/>
        </div>
      </div>
    </div>
  </div>
</div>
