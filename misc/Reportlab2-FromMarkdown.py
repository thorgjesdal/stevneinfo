#!/usr/bin/env python
# coding: utf-8

# #Markdown 2 Reportlab

# ## Markdown
# Here we create some lorem ipsum markdown text for testing

# In[1]:


from IPython.display import HTML
import markdown as md


# In[2]:


l = """LOREM ipsum dolor sit amet, _consectetur_ adipiscing elit. Praesent dignissim orci a leo dapibus semper eget sed 
sem. Pellentesque tellus nisl, condimentum nec libero id, __cursus consequat__ lectus. Ut quis nulla laoreet, efficitur 
metus sit amet, <strike>viverra dui. Nam tempor ornare urna a consequat</strike>. Nulla dolor velit, sollicitudin sit 
amet consectetur sed, interdum nec orci. Nunc suscipit tempus est ut porta. <u>Ut non felis a ligula suscipit 
posuere quis sit amet elit</u>."""

markdown_text = """
# Heading1
## Heading 2

%s %s %s


## Heading 2

%s

- %s
- %s
- %s

## Heading 2

%s

4. %s
4. %s
4. %s

%s
""" % (l,l,l,l,l,l,l,l,l,l,l,l)


# In[3]:


#HTML(md.markdown(markdown_text))


# ## ReportLab
# import the necessary functions one by one

# In[4]:


from markdown import markdown as md_markdown

from xml.etree.ElementTree import fromstring as et_fromstring
from xml.etree.ElementTree import tostring as et_tostring

from reportlab.platypus import BaseDocTemplate as plat_BaseDocTemplate
from reportlab.platypus import Frame as plat_Frame
from reportlab.platypus import Paragraph as plat_Paragraph
from reportlab.platypus import PageTemplate as plat_PageTemplate

from reportlab.lib.styles import getSampleStyleSheet as sty_getSampleStyleSheet
from reportlab.lib.pagesizes import A4 as ps_A4
from reportlab.lib.pagesizes import A5 as ps_A5
from reportlab.lib.pagesizes import landscape as ps_landscape
from reportlab.lib.pagesizes import portrait as ps_portrait
from reportlab.lib.units import inch as un_inch


# The `ReportFactory` class creates a ReportLab document / report object; the idea is that all style information as well as page layouts are collected in this object, so that when a different factory is passed to the writer object the report looks different.

# In[5]:


class ReportFactory():
    """create a Reportlab report object using BaseDocTemplate
    
    the report creation is a two-step process
    
    1. instantiate a ReportFactory object
    2. retrieve the report using the report() method
    
    note: as it currently stands the report object is remembered in the
    factory object, so another call to report() return the _same_ object;
    this means that changing the paramters after report() has been called
    for the first time will not have an impact
    """
    
    def __init__(self, filename=None):      
        if filename == None: filename = 'report_x1.pdf'
        # f = open (filename,'wb') -> reports can take a file handle!
        self.filename = filename
        self.pagesize = ps_portrait(ps_A4)
        self.showboundary = 0
        #PAGE_HEIGHT=defaultPageSize[1]; PAGE_WIDTH=defaultPageSize[0]
        self.styles=sty_getSampleStyleSheet()
        self.bullet = "\u2022"
        self._report = None
 
    @staticmethod
    def static_page(canvas,doc):
        """template for report page
        
        this template defines how the standard page looks (header, footer, background
        objects; it does _not_ define the flow objects though, as those are separately
        passed to the PageTemplate() function)
        """
        canvas.saveState()
        canvas.setFont('Times-Roman',9)
        canvas.drawString(un_inch, 0.75 * un_inch, "Report - Page %d" % doc.page)
        canvas.restoreState()
    
    def refresh_styles(self):
        """refresh all styles
        
        derived ReportLab styles need to be refreshed in case the parent style
        has been modified; this does not really work though - it seems that the
        styles are simply flattened....
        """
        style_names = self.styles.__dict__['byName'].keys()
        for name in style_names:
            self.styles[name].refresh()
            
    def report(self):
        """initialise a report object
        
        this function initialised and returns a report object, based on the properties
        set on the factory object at this point (note: the report object is only generated
        _once_ and subsequent calls return the same object;this implies that most property
        changes after this function has been called are not taken into account)
        """
        if self._report == None:
            rp = plat_BaseDocTemplate(self.filename,showBoundary=self.showboundary, pagesize=self.pagesize)
            frame_page = plat_Frame(rp.leftMargin, rp.bottomMargin, rp.width, rp.height, id='main')
            pagetemplates = [
                plat_PageTemplate(id='Page',frames=frame_page,onPage=self.static_page),
            ]
            rp.addPageTemplates(pagetemplates)
            self._report = rp
        return self._report

        


# The `ReportWriter` object executes the conversion from markdown to pdf. It is currently very simplistic - for example there is no entry hook for starting the conversion at the html level rather than at markdown, and only a few basic tags are implemented. 

# In[6]:


class ReportWriter():
    
    def __init__(self, report_factory):
        self._simple_tags = {
            'h1'     : 'Heading1',
            'h2'     : 'Heading2',
            'h3'     : 'Heading3',
            'h4'     : 'Heading4',
            'h5'     : 'Heading5',
            'p'      : 'BodyText',
        }
        self.rf = report_factory
        self.report = report_factory.report();
        
    def _render_simple_tag(self, el, story):
        style_name = self._simple_tags[el.tag]
        el.tag = 'para'
        text = et_tostring(el)
        story.append(plat_Paragraph(text,self.rf.styles[style_name]))
        
    def _render_ol(self, el, story):
        return self._render_error(el, story)
    
    def _render_ul(self, ul_el, story):
        for li_el in ul_el:
            li_el.tag = 'para'
            text = et_tostring(li_el)
            story.append(plat_Paragraph(text,self.rf.styles['Bullet'], bulletText=self.rf.bullet))
    
    def _render_error(self, el, story):
        story.append(plat_Paragraph(
            "<para fg='#ff0000' bg='#ffff00'>cannot render '%s' tag</para>" % el.tag,self.rf.styles['Normal']))
    
    @staticmethod
    def html_from_markdown(mdown, remove_newline=True, wrap=True):
        """convert markdown to html
        
        mdown - the markdown to be converted
        remove_newline - if True, all \n characters are removed after conversion
        wrap - if True, the whole html is wrapped in an <html> tag
        """
        html = md_markdown(mdown)
        if remove_newline: html = html.replace("\n", "")
        if wrap: html = "<html>"+html+"</html>"
        return html
    
    @staticmethod
    def dom_from_html(html, wrap=False):
        """convert html into a dom tree
        
        html - the html to be converted
        wrap - if True, the whole html is wrapped in an <html> tag 
        """
        if wrap: html = "<html>"+html+"</html>"
        dom = et_fromstring(html)
        return (dom)
    
    @staticmethod
    def dom_from_markdown(mdown):
        """convert markdown into a dom tree
        
        mdown - the markdown to be converted
        wrap - if True, the whole html is wrapped in an <html> tag 
        """
        html = ReportWriter.html_from_markdown(mdown, remove_newline=True, wrap=True)
        dom = ReportWriter.dom_from_html(html, wrap=False)
        return (dom)
    
    def create_report(self, mdown):
        """create report and write it do disk
        
        mdown - markdown source of the report
        """
        dom = self.dom_from_markdown(mdown)
        story = []
        for el in dom:
            if el.tag in self._simple_tags:
                self._render_simple_tag(el, story)
            elif el.tag == 'ul':
                self._render_ul(el, story)
            elif el.tag == 'ol':
                self._render_ol(el, story)
            else:
                self._render_error(el, story)
        self.report.build(story)


# create a standard report (A4, black text etc)

# In[7]:


rfa4 = ReportFactory('report_a4.pdf')
pdfw = ReportWriter(rfa4)
pdfw.create_report(markdown_text*10)


# create a second report with different parameters (A5, changed colors etc; the `__dict__` method shows all the options that can be modified for changing styles)

# In[8]:


#rfa5.styles['Normal'].__dict__


# In[9]:


rfa5 = ReportFactory('report_a5.pdf')
rfa5.pagesize = ps_portrait(ps_A5)
#rfa5.styles['Normal'].textColor = '#664422'
#rfa5.refresh_styles()
rfa5.styles['BodyText'].textColor = '#666666'
rfa5.styles['Bullet'].textColor   = '#666666'
rfa5.styles['Heading1'].textColor = '#000066'
rfa5.styles['Heading2'].textColor = '#000066'
rfa5.styles['Heading3'].textColor = '#000066'


# In[10]:


pdfw = ReportWriter(rfa5)
pdfw.create_report(markdown_text*10)


# <a style='text-decoration:none;line-height:16px;display:flex;color:#5B5B62;padding:10px;justify-content:end;' href='https://deepnote.com?utm_source=created-in-deepnote-cell&projectId=c6ee82c6-048a-4f91-85a5-434b26f336b8' target="_blank">
# <img alt='Created in deepnote.com' style='display:inline;max-height:16px;margin:0px;margin-right:7.5px;' src='data:image/svg+xml;base64,PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0iVVRGLTgiPz4KPHN2ZyB3aWR0aD0iODBweCIgaGVpZ2h0PSI4MHB4IiB2aWV3Qm94PSIwIDAgODAgODAiIHZlcnNpb249IjEuMSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIiB4bWxuczp4bGluaz0iaHR0cDovL3d3dy53My5vcmcvMTk5OS94bGluayI+CiAgICA8IS0tIEdlbmVyYXRvcjogU2tldGNoIDU0LjEgKDc2NDkwKSAtIGh0dHBzOi8vc2tldGNoYXBwLmNvbSAtLT4KICAgIDx0aXRsZT5Hcm91cCAzPC90aXRsZT4KICAgIDxkZXNjPkNyZWF0ZWQgd2l0aCBTa2V0Y2guPC9kZXNjPgogICAgPGcgaWQ9IkxhbmRpbmciIHN0cm9rZT0ibm9uZSIgc3Ryb2tlLXdpZHRoPSIxIiBmaWxsPSJub25lIiBmaWxsLXJ1bGU9ImV2ZW5vZGQiPgogICAgICAgIDxnIGlkPSJBcnRib2FyZCIgdHJhbnNmb3JtPSJ0cmFuc2xhdGUoLTEyMzUuMDAwMDAwLCAtNzkuMDAwMDAwKSI+CiAgICAgICAgICAgIDxnIGlkPSJHcm91cC0zIiB0cmFuc2Zvcm09InRyYW5zbGF0ZSgxMjM1LjAwMDAwMCwgNzkuMDAwMDAwKSI+CiAgICAgICAgICAgICAgICA8cG9seWdvbiBpZD0iUGF0aC0yMCIgZmlsbD0iIzAyNjVCNCIgcG9pbnRzPSIyLjM3NjIzNzYyIDgwIDM4LjA0NzY2NjcgODAgNTcuODIxNzgyMiA3My44MDU3NTkyIDU3LjgyMTc4MjIgMzIuNzU5MjczOSAzOS4xNDAyMjc4IDMxLjY4MzE2ODMiPjwvcG9seWdvbj4KICAgICAgICAgICAgICAgIDxwYXRoIGQ9Ik0zNS4wMDc3MTgsODAgQzQyLjkwNjIwMDcsNzYuNDU0OTM1OCA0Ny41NjQ5MTY3LDcxLjU0MjI2NzEgNDguOTgzODY2LDY1LjI2MTk5MzkgQzUxLjExMjI4OTksNTUuODQxNTg0MiA0MS42NzcxNzk1LDQ5LjIxMjIyODQgMjUuNjIzOTg0Niw0OS4yMTIyMjg0IEMyNS40ODQ5Mjg5LDQ5LjEyNjg0NDggMjkuODI2MTI5Niw0My4yODM4MjQ4IDM4LjY0NzU4NjksMzEuNjgzMTY4MyBMNzIuODcxMjg3MSwzMi41NTQ0MjUgTDY1LjI4MDk3Myw2Ny42NzYzNDIxIEw1MS4xMTIyODk5LDc3LjM3NjE0NCBMMzUuMDA3NzE4LDgwIFoiIGlkPSJQYXRoLTIyIiBmaWxsPSIjMDAyODY4Ij48L3BhdGg+CiAgICAgICAgICAgICAgICA8cGF0aCBkPSJNMCwzNy43MzA0NDA1IEwyNy4xMTQ1MzcsMC4yNTcxMTE0MzYgQzYyLjM3MTUxMjMsLTEuOTkwNzE3MDEgODAsMTAuNTAwMzkyNyA4MCwzNy43MzA0NDA1IEM4MCw2NC45NjA0ODgyIDY0Ljc3NjUwMzgsNzkuMDUwMzQxNCAzNC4zMjk1MTEzLDgwIEM0Ny4wNTUzNDg5LDc3LjU2NzA4MDggNTMuNDE4MjY3Nyw3MC4zMTM2MTAzIDUzLjQxODI2NzcsNTguMjM5NTg4NSBDNTMuNDE4MjY3Nyw0MC4xMjg1NTU3IDM2LjMwMzk1NDQsMzcuNzMwNDQwNSAyNS4yMjc0MTcsMzcuNzMwNDQwNSBDMTcuODQzMDU4NiwzNy43MzA0NDA1IDkuNDMzOTE5NjYsMzcuNzMwNDQwNSAwLDM3LjczMDQ0MDUgWiIgaWQ9IlBhdGgtMTkiIGZpbGw9IiMzNzkzRUYiPjwvcGF0aD4KICAgICAgICAgICAgPC9nPgogICAgICAgIDwvZz4KICAgIDwvZz4KPC9zdmc+' > </img>
# Created in <span style='font-weight:600;margin-left:4px;'>Deepnote</span></a>
