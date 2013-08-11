require 'readmore'
require 'erubis'
require 'tilt'

Awestruct::Extensions::Pipeline.new do
  extension Awestruct::Extensions::Posts.new( '/posts', :posts)
  extension Awestruct::Extensions::Paginator.new( :posts, '/index', :per_page => 5 )
  extension Awestruct::Extensions::Tagger.new( :posts, '/index', '/posts/tags', :per_page => 10)
#  extension Awestruct::Extensions::TagCloud.new( :tagcloud, '/posts/tags/index.html', :layout=>'base', :title=>'Tags')
  extension Awestruct::Extensions::Disqus.new

  extension Awestruct::Extensions::Indexifier.new
  extension Awestruct::Extensions::Atomizer.new( :posts, '/atom.xml', :feed_title=>'goldstift\'s blog' )

  helper Awestruct::Extensions::Partial
  helper Awestruct::Extensions::ReadMore
end